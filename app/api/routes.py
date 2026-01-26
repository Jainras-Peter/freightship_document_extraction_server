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

    # 2. Preprocess (Get Images)
    images = []
    try:
        if file_type == "pdf":
            images = convert_pdf_to_images(contents)
        else:
            # Image
            import io
            image = Image.open(io.BytesIO(contents))
            images = [image]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing failed: {str(e)}")

    if not images:
         raise HTTPException(status_code=400, detail="No images could be processed from the file.")

    # 3. OCR (Accumulate text from all pages)
    full_text = ""
    try:
        for img in images:
            text = perform_ocr(img)
            full_text += text + "\n\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

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
