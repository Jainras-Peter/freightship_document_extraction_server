# app/ai_agent/core/embeddings.py
# Embeddings generator supporting API or local transformer models
import cohere
from app.config import settings

class CohereEmbeddings:
    def __init__(self, model_name="embed-english-v3.0"):
        self.model_name = model_name
        self.client = cohere.Client(api_key=settings.COHERE_API_KEY)

    def embed_query(self, text: str) -> list[float]:
        # Cohere v3 requires input_type
        response = self.client.embed(
            texts=[text],
            model=self.model_name,
            input_type="search_query"
        )
        return response.embeddings[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Cohere handles bulk efficiently
        response = self.client.embed(
            texts=texts,
            model=self.model_name,
            input_type="search_document"
        )
        return response.embeddings

