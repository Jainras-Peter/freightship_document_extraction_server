# app/ai_agent/agents/help_qa.py
# Help QA SOP Agent pulling static support data via Vector Store
import os
from pathlib import Path
from groq import Groq
from app.config import settings
from app.ai_agent.core.embeddings import CohereEmbeddings
from app.ai_agent.vectordb.faiss import FAISSDriver
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

class HelpQAAgent:
    def __init__(self, project_id: str = "freightship"):
        self.project_id = project_id
        
        # Determine Path to FAISS index
        base_dir = Path(__file__).parent.parent
        self.index_path = base_dir / "projects" / project_id / "data" / "faiss_index"
        
        # Use Cohere for Embeddings
        self.embeddings = CohereEmbeddings(model_name="embed-english-v3.0")
        self.vector_db = FAISSDriver(index_path=str(self.index_path), embeddings_model=self.embeddings)
        
        # Use Groq for lightning fast LLM Generation (bypassing ISP HF Blocks)
        api_key = settings.GROQ_API_KEY
        if not api_key:
             logger.warning("GROQ_API_KEY is not set. Inference API might fail.")
             
        self.llm_client = Groq(api_key=api_key)
        self.llm_model = "llama-3.1-8b-instant"

    def index_document(self, text: str, filename: str):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        formatted_chunks = [f"Source: {filename}\n{chunk}" for chunk in chunks]
        
        logger.info(f"Indexing {len(formatted_chunks)} chunks for {filename}...")
        self.vector_db.add_texts(formatted_chunks)

    def generate(self, user_input: str) -> str:
        logger.info(f"Retrieving context for query: {user_input}")
        contexts = self.vector_db.similarity_search(user_input, k=3)
        
        if not contexts:
            context_str = "No relevant context found."
        else:
            context_str = "\n\n---\n\n".join(contexts)
        
        prompt = f"""You are a helpful assistant for the project '{self.project_id}'.
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer based on the context, just say that you don't know.

Context:
{context_str}

Question:
{user_input}

Answer:"""

        logger.info("Calling Groq LLM for generation...")
        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
