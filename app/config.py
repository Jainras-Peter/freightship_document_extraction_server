import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    #Engines
    EXTRACTION_ENGINE = os.getenv("EXTRACTION_ENGINE", "groq")
    OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
    #API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    # URL
    HUGGINGFACE_BASE_URL = os.getenv("HUGGINGFACE_BASE_URL", "https://router.huggingface.co/v1") 
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    
    # Database / Cache
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "document_extractor_cache")
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "False").lower() == "true"

    #Debug
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
