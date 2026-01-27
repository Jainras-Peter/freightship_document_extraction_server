from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
import shutil
import os
import uuid
from PIL import Image

from app.controllers.input_validator import validate_file
from app.preprocess.image_extractor import convert_pdf_to_images
from app.ocr.tesseract_ocr import perform_ocr
from app.extractor_engine.factory import get_extractor
from app.core.debug import save_debug_artifacts
from app.config import settings

router = APIRouter()

@router.post("/extract")
async def extract_document(
    file: UploadFile = File(...),
    schema: str = Form(...),
    debug: bool = Form(False)
):
    request_id = str(uuid.uuid4())
    file_type = validate_file(file)
    
    # 1. Read File
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    # 2. Preprocess & 3. OCR (Unified Logic)
    images = []
    full_text = ""
    ocr_engine = settings.OCR_ENGINE.lower()

    try:
        # Check if we should use Direct Text Extraction (Only for PDF + Configured)
        if file_type == "pdf" and ocr_engine == "pdf_text":
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

    # 4. Parse Schema
    try:
        schema_dict = json.loads(schema)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON schema provided.")

    # 5. Extraction
    try:
        extractor = get_extractor()
        result = extractor.extract(full_text, schema_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    # 6. Debug / Save Artifacts
    # Use global setting OR request param
    should_debug = debug or settings.DEBUG
    if should_debug:
        save_debug_artifacts(request_id, images, full_text, result)

    return result
