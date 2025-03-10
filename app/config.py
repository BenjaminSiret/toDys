import os
from functools import lru_cache
from pathlib import Path
from typing import List, Set

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import DirectoryPath, PositiveInt

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Settings(BaseModel):
    # App Info
    APP_TITLE: str = "toDys"
    APP_DESCRIPTION: str = "Application de transformation de documents pour la dyslexie"
    APP_VERSION: str = "1.0.0"

    # Environment
    ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: PositiveInt = 8000

    # Upload
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))
    ALLOWED_EXTENSIONS: Set[str] = {"pdf", "docx", "doc", "odt", "txt", "rtf"}
    UPLOAD_DIR: DirectoryPath = Path("uploads")

    # API Keys
    API_KEY_HUGGING_FACE: str = ""

    # Sécurité
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    RATE_LIMIT_PER_MINUTE: PositiveInt = 60

    # Logging
    LOG_LEVEL: str = "INFO"

    @field_validator("UPLOAD_DIR")
    def create_upload_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v

    class Config:
        model_config = ConfigDict(
            env_file='.env',
            env_file_encoding='utf-8',
            case_sensitive=True
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
