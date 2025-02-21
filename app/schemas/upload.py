"""
Schémas Pydantic pour la validation des uploads de fichiers.
"""
from typing import Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """Réponse de l'API pour les uploads de fichiers."""
    success: bool
    message: str
    filename: Optional[str] = None
    file_url: Optional[str] = None
    mime_type: Optional[str] = None
    error: Optional[str] = None
