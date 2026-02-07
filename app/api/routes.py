from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
import shutil
import os
import uuid
import logging
from PIL import Image

from app.controllers.input_validator import validate_file
from app.preprocess.image_extractor import convert_pdf_to_images
from app.ocr.tesseract_ocr import perform_ocr
from app.extractor_engine.factory import get_extractor
from app.core.debug import save_debug_artifacts
from app.config import settings

# Initialize Logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/extract")
async def extract_document(
    file: UploadFile = File(...),
    json_schema: str = Form(..., alias="schema"),
    extraction_engine: str = Form("groq"),
    ocr_engine: str = Form("tesseract"),
    debug: bool = Form(False)
):
    request_id = str(uuid.uuid4())
    file_type = validate_file(file)
    
    # 1. Read File
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    # Parse Schema early for hashing
    try:
        schema_dict = json.loads(json_schema)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON schema provided.")

    # Caching Logic
    file_hash = None
    schema_hash = None
    
    if settings.CACHE_ENABLED:
        try:
            from app.utils.hashing import compute_file_hash, compute_schema_hash
            from app.services.cache_service import cache_service
            
            file_hash = compute_file_hash(contents)
            schema_hash = compute_schema_hash(schema_dict)
            
            cached_result = await cache_service.get_cached_result(file_hash, schema_hash)
            if cached_result:
                logger.info(f"FROM CACHE: Request {request_id} served from DB.")
                return cached_result['extracted_data']
            else:
                 logger.info(f"CACHE MISS: Request {request_id} proceeding to LLM / Processing.")
        except Exception as e:
            logger.error(f"Cache check failed: {e}")

    # --- PROCESSING STARTS (Cache Miss or Disabled) ---
    logger.info(f"FROM LLM: Request {request_id} being processed using {extraction_engine} and {ocr_engine} - {file.filename}")

    # 2. Preprocess & 3. OCR (Unified Logic)
    images = []
    full_text = ""
    # Use payload ocr_engine, default to settings if somehow empty or not provided (schema has default though)
    selected_ocr_engine = ocr_engine.lower() if ocr_engine else settings.OCR_ENGINE.lower()

    try:
        # Check if we should use Direct Text Extraction (Only for PDF + Configured)
        if file_type == "pdf" and selected_ocr_engine == "pdf_text":
            from app.preprocess.pdf_text_extractor import extract_text_from_pdf
            full_text = extract_text_from_pdf(contents)
            
            # NOTE: We skip image generation here as requested for performance.
            # artifacts will only contain text and JSON.
            
        else:
            # Fallback / Default: Image Conversion + OCR
            if file_type == "pdf":
                images = convert_pdf_to_images(contents)
            else:
                # Image file
                import io
                image = Image.open(io.BytesIO(contents))
                images = [image]
            
            if not images:
                 raise HTTPException(status_code=400, detail="No images could be processed from the file.")

            for img in images:
                text = perform_ocr(img)
                full_text += text + "\n\n"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    # 4. Parse Schema (Alredy done above)
    # kept purely for flow if logic changes, but variable schema_dict is already available.

    # 5. Extraction
    try:
        extractor = get_extractor(engine_name=extraction_engine)
        result = extractor.extract(full_text, schema_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    # 5. Save to Cache
    if settings.CACHE_ENABLED and file_hash and schema_hash:
        try:
             # Importing here to ensure visibility or rely on top imports if moved
             from app.services.cache_service import cache_service
             await cache_service.save_result(file_hash, schema_hash, result)
        except Exception as e:
             logger.error(f"Failed to save to cache: {e}")

    # 6. Debug / Save Artifacts
    # Use global setting OR request param
    should_debug = debug or settings.DEBUG
    if should_debug:
        save_debug_artifacts(request_id, images, full_text, result)

    return result
