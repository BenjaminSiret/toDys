import os
from pathlib import Path
from typing import List, Set

from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from pydantic.types import DirectoryPath, PositiveInt

# Charger les variables d'environnement
load_dotenv()

class Settings(BaseModel):
    # App Info
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str

    # Environment
    ENV: str
    DEBUG: bool
    HOST: str
    PORT: PositiveInt

    # Upload
    MAX_UPLOAD_SIZE: PositiveInt
    ALLOWED_EXTENSIONS: Set[str]
    UPLOAD_DIR: DirectoryPath

    # API Keys
    API_KEY_HUGGING_FACE: str

    # Nouveaux paramètres de sécurité
    CORS_ORIGINS: List[str]
    RATE_LIMIT_PER_MINUTE: PositiveInt

    # Logging
    LOG_LEVEL: str

    @validator("UPLOAD_DIR")
    def create_upload_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Instance unique avec les valeurs par défaut
settings = Settings(
    APP_TITLE="toDys",
    APP_DESCRIPTION="Application de transformation de documents pour la dyslexie",
    APP_VERSION="1.0.0",
    ENV=os.getenv("ENV", "development"),
    DEBUG=os.getenv("DEBUG", "True").lower() == "true",
    HOST=os.getenv("HOST", "0.0.0.0"),
    PORT=int(os.getenv("PORT", "8000")),
    MAX_UPLOAD_SIZE=int(os.getenv("MAX_UPLOAD_SIZE", str(10 * 1024 * 1024))),
    ALLOWED_EXTENSIONS={"pdf", "docx", "doc", "odt", "txt", "rtf"},
    UPLOAD_DIR=Path(os.getenv("UPLOAD_DIR", "uploads")),
    API_KEY_HUGGING_FACE=os.getenv("API_KEY_HUGGING_FACE", ""),
    CORS_ORIGINS=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    RATE_LIMIT_PER_MINUTE=int(os.getenv("RATE_LIMIT", "60")),
    LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO")
)
