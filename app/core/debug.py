import os
import time
from PIL import Image
import json

def save_debug_artifacts(request_id: str, images: list, ocr_text: str, extracted_json: dict = None):
    """
    Save debug artifacts to debug_output/{timestamp}_{request_id}/
    """
    if not os.path.exists("debug_output"):
        os.makedirs("debug_output")
    
    timestamp = int(time.time())
    folder_name = f"{timestamp}_{request_id}"
    folder_path = os.path.join("debug_output", folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    
    # Save Images
    for idx, img in enumerate(images):
        img_path = os.path.join(folder_path, f"page_{idx+1}.png")
        img.save(img_path)
    
    # Save OCR Text
    with open(os.path.join(folder_path, "ocr_text.txt"), "w", encoding="utf-8") as f:
        f.write(ocr_text)
        
    # Save extracted JSON if available
    if extracted_json:
        with open(os.path.join(folder_path, "result.json"), "w", encoding="utf-8") as f:
            json.dump(extracted_json, f, indent=2)

    print(f"DEBUG: Artifacts saved to {folder_path}")
