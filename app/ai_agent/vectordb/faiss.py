# app/ai_agent/vectordb/faiss.py
# Persistent Local FAISS implementation for static help SOP RAG
import faiss
import numpy as np
import pickle
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FAISSDriver:
    def __init__(self, index_path: str, embeddings_model):
        self.index_path = Path(index_path)
        self.index_file = self.index_path / "index.faiss"
        self.meta_file = self.index_path / "meta.pkl"
        self.embeddings_model = embeddings_model
        
        self.index = None
        self.texts = []
        
        if self.index_file.exists() and self.meta_file.exists():
            self.load()
        else:
            self.index_path.mkdir(parents=True, exist_ok=True)
            # Default to 1024 dimensions for Cohere embed-english-v3.0
            self.index = faiss.IndexFlatL2(1024)

    def add_texts(self, texts: list[str]):
        if not texts:
            return
        
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embeddings_model.embed_documents(texts)
        embeddings_np = np.array(embeddings).astype('float32')
        
        self.index.add(embeddings_np)
        self.texts.extend(texts)
        self.save()
        logger.info(f"Successfully added {len(texts)} chunks to FAISS index.")

    def similarity_search(self, query: str, k: int = 3) -> list[str]:
        if self.index.ntotal == 0:
            return []
            
        query_embedding = self.embeddings_model.embed_query(query)
        # Ensure embedding is 2D for FAISS search
        if len(np.array(query_embedding).shape) == 1:
            query_embedding = [query_embedding]
            
        query_np = np.array(query_embedding).astype('float32')
        distances, indices = self.index.search(query_np, k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.texts):
                results.append(self.texts[idx])
        return results

    def save(self):
        faiss.write_index(self.index, str(self.index_file))
        with open(self.meta_file, 'wb') as f:
            pickle.dump(self.texts, f)

    def load(self):
        try:
            self.index = faiss.read_index(str(self.index_file))
            with open(self.meta_file, 'rb') as f:
                self.texts = pickle.load(f)
            logger.info(f"Loaded FAISS index from {self.index_path} with {self.index.ntotal} items.")
        except Exception as e:
            logger.error(f"Failed to load FAISS index: {e}")
            self.index = faiss.IndexFlatL2(1024)
            self.texts = []
