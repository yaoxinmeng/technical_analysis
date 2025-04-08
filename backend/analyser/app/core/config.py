from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = "debug"
    MONGO_INITDB_ROOT_USERNAME: str 
    MONGO_INITDB_ROOT_PASSWORD: str 
    MONGO_ENDPOINT: str 

settings = Settings()