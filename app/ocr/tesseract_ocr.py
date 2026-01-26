import pytesseract
from PIL import Image

def perform_ocr(image: Image.Image) -> str:
    text = pytesseract.image_to_string(image)
    return text
