import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EXTRACTION_ENGINE = os.getenv("EXTRACTION_ENGINE", "groq")
    OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
