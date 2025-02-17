"""
Service de validation des fichiers pour toDys.
"""
from pathlib import Path
import magic
from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile
from ..config import get_settings

settings = get_settings()

class ValidationResult(BaseModel):
    """Résultat de la validation d'un fichier."""
    is_valid: bool
    error_message: Optional[str] = None
    mime_type: Optional[str] = None
    file_path: Optional[Path] = None

class FileValidator:
    """
    Validateur de fichiers avec vérifications de sécurité.
    
    Caractéristiques:
    - Validation MIME type
    - Vérification de la taille
    - Vérification des extensions
    - Détection de contenu malveillant basique
    """
    
    def __init__(self):
        self.magic = magic.Magic(mime=True)
        self._ensure_upload_dir()

    async def validate_file(self, file: UploadFile) -> ValidationResult:
        """
        Valide un fichier uploadé selon plusieurs critères de sécurité.
        
        Args:
            file: Le fichier à valider
            
        Returns:
            ValidationResult: Résultat de la validation
        """
        # Vérification du nom de fichier
        if not file.filename:
            return ValidationResult(
                is_valid=False,
                error_message="Nom de fichier manquant"
            )

        # Vérification de l'extension
        extension = Path(file.filename).suffix[1:].lower()
        if extension not in settings.ALLOWED_EXTENSIONS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Extension .{extension} non autorisée"
            )

        # Lecture du contenu pour validation
        content = await file.read(settings.MAX_UPLOAD_SIZE + 1)
        
        # Vérification de la taille
        if len(content) > settings.MAX_UPLOAD_SIZE:
            await file.seek(0)
            return ValidationResult(
                is_valid=False,
                error_message=f"Le fichier dépasse la taille maximale de {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
            )

        # Vérification du type MIME
        mime_type = self.magic.from_buffer(content)
        await file.seek(0)

        # Vérification du contenu malveillant
        if self._detect_malicious_content(content):
            return ValidationResult(
                is_valid=False,
                error_message="Le fichier semble malveillant"
            )

        return ValidationResult(
            is_valid=True,
            mime_type=mime_type,
            file_path=self._get_upload_path(file.filename)
        )

    def _ensure_upload_dir(self):
        """S'assure que le dossier d'upload existe."""
        settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def _get_upload_path(self, filename: str) -> Path:
        """Génère un chemin sécurisé pour le fichier uploadé."""
        safe_filename = Path(filename).name  # Utilise seulement le nom du fichier
        return settings.UPLOAD_DIR / safe_filename

    def _detect_malicious_content(self, content: bytes) -> bool:
        """
        Détecte les contenus potentiellement malveillants.
        
        Args:
            content: Contenu du fichier
            
        Returns:
            bool: True si le contenu semble malveillant
        """
        # Liste de signatures malveillantes (à enrichir)
        malicious_signatures = [
            b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$',  # EICAR test signature
            b'#!/',  # Scripts shell
            b'<?php',  # Code PHP
        ]
        
        return any(sig in content for sig in malicious_signatures)
