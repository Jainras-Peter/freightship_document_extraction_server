from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from typing import List
import io

def convert_pdf_to_images(file_bytes: bytes) -> List[Image.Image]:
    images = convert_from_bytes(file_bytes)
    return images
