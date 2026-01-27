import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            logging.info("Connected to MongoDB via Motor.")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            self.client = None

    def close(self):
        if self.client:
            self.client.close()
            logging.info("Closed MongoDB connection.")

    def get_db(self):
        if self.client:
            return self.client[settings.DB_NAME]
        return None

db = Database()
