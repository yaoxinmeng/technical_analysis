from pymongo import MongoClient
from app.core.config import settings

class MongoDb:
    def __init__(self, db_name: str, collection_name: str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        self.client = MongoClient(
            settings.MONGO_ENDPOINT, 
            username=settings.MONGO_INITDB_ROOT_USERNAME, 
            password=settings.MONGO_INITDB_ROOT_PASSWORD
        )
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close(self):
        if self.client:
            self.client.close()