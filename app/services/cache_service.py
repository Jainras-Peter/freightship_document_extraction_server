from datetime import datetime
from app.core.database import db
import logging

class CacheService:
    def __init__(self):
        self.collection_name = "extraction_cache"

    async def get_cached_result(self, file_hash: str, schema_hash: str):
        """Retrieve result from cache if exists."""
        db_instance = db.get_db()
        if db_instance is None:
            logging.warning("Database not connected. Skipping cache check.")
            return None
            
        collection = db_instance[self.collection_name]
        return await collection.find_one({
            "file_hash": file_hash, 
            "schema_hash": schema_hash
        })

    async def save_result(self, file_hash: str, schema_hash: str, result: dict):
        """Save extraction result to cache."""
        db_instance = db.get_db()
        if db_instance is None:
            logging.warning("Database not connected. Skipping cache save.")
            return

        collection = db_instance[self.collection_name]
        
        document = {
            "file_hash": file_hash,
            "schema_hash": schema_hash,
            "extracted_data": result,
            "created_at": datetime.utcnow()
        }
        
        await collection.insert_one(document)
        logging.info(f"Saved result to cache for FileHash: {file_hash[:8]}...")

cache_service = CacheService()
