from app.config import settings
from .groq.extractor import GroqExtractor
from .ollama.extractor import OllamaExtractor
import os

def get_extractor():
    engine = settings.EXTRACTION_ENGINE.lower()

    if engine == "groq":
        return GroqExtractor()
    elif engine == "ollama":
        return OllamaExtractor()
    else:
        raise ValueError(f"Unsupported extraction engine: {engine}")
