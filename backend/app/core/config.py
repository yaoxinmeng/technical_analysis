from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = "debug"
    PLAYWRIGHT_TIMEOUT: int = 10000  # in milliseconds

settings = Settings()