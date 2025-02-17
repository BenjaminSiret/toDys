"""
Service de validation des fichiers pour toDys.
Fournit des fonctionnalités de validation sécurisée des fichiers uploadés.
"""
import os
from dataclasses import dataclass
from typing import Optional, Tuple

import magic
from werkzeug.datastructures import FileStorage


@dataclass
class ValidationResult:
    """Résultat de la validation d'un fichier."""
    is_valid: bool
    error_message: Optional[str] = None
    mime_type: Optional[str] = None

class FileValidator:
    """
    Validateur de fichiers avec vérifications de sécurité.

    Caractéristiques:
    - Validation MIME type
    - Vérification de la taille
    - Vérification des extensions
    - Détection de contenu malveillant basique
    """

    # Types MIME autorisés et leurs extensions correspondantes
    ALLOWED_MIMES = {
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.oasis.opendocument.text': '.odt',
        'text/plain': '.txt'
    }

    # Taille maximale de fichier (10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    def __init__(self):
        self.magic = magic.Magic(mime=True)

    def validate_file(self, file: FileStorage) -> ValidationResult:
        """
        Valide un fichier uploadé selon plusieurs critères de sécurité.

        Args:
            file: Le fichier à valider

        Returns:
            ValidationResult: Résultat de la validation avec message d'erreur si invalide
        """
        # Vérification de la taille
        if not self._check_file_size(file):
            return ValidationResult(
                is_valid=False,
                error_message=f"Le fichier dépasse la taille maximale de {self.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Vérification du type MIME
        mime_type = self._get_mime_type(file)
        if not self._is_allowed_mime_type(mime_type):
            return ValidationResult(
                is_valid=False,
                error_message="Type de fichier non autorisé"
            )

        # Vérification de l'extension
        if not self._validate_extension(file.filename, mime_type):
            return ValidationResult(
                is_valid=False,
                error_message="L'extension du fichier ne correspond pas à son contenu"
            )

        # Vérification du contenu malveillant
        if self._detect_malicious_content(file):
            return ValidationResult(
                is_valid=False,
                error_message="Le fichier semble malveillant"
            )

        return ValidationResult(
            is_valid=True,
            mime_type=mime_type
        )

    def _check_file_size(self, file: FileStorage) -> bool:
        """Vérifie si la taille du fichier est dans les limites."""
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)  # Réinitialise le curseur
        return size <= self.MAX_FILE_SIZE

    def _get_mime_type(self, file: FileStorage) -> str:
        """Détecte le type MIME réel du fichier."""
        # Sauvegarde temporaire pour analyse
        temp_path = file.stream.read()
        mime_type = self.magic.from_buffer(temp_path)
        file.stream.seek(0)  # Réinitialise le curseur
        return mime_type

    def _is_allowed_mime_type(self, mime_type: str) -> bool:
        """Vérifie si le type MIME est autorisé."""
        return mime_type in self.ALLOWED_MIMES

    def _validate_extension(self, filename: str, mime_type: str) -> bool:
        """Vérifie si l'extension correspond au type MIME."""
        if not filename or '.' not in filename:
            return False

        extension = os.path.splitext(filename)[1].lower()
        return self.ALLOWED_MIMES.get(mime_type) == extension

    def _detect_malicious_content(self, file: FileStorage) -> bool:
        """
        Détecte les contenus potentiellement malveillants.

        Note: Cette implémentation est basique et devrait être enrichie
        avec des règles plus sophistiquées en production.
        """
        # Vérifie les signatures de fichiers malveillants connus
        content = file.stream.read(4096)  # Lit les premiers 4KB
        file.stream.seek(0)  # Réinitialise le curseur

        # Liste de signatures malveillantes (à enrichir)
        malicious_signatures = [
            b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$',  # EICAR test signature
            b'#!/',  # Scripts shell
            b'<?php',  # Code PHP
        ]

        return any(sig in content for sig in malicious_signatures)
