import asyncio
import logging
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.services.file_validator import ValidationResult
from app.services.supabase_service import SupabaseService

client = TestClient(app)
settings = get_settings()
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_upload_success(mock_file):
    # Préparer les mocks
    mock_validator = AsyncMock()
    mock_validator.validate_file.return_value = ValidationResult(is_valid=True)

    mock_service = AsyncMock(spec=SupabaseService)
    mock_service.upload_file.return_value = {
        "file_name": "test.pdf",
        "file_url": "http://test.url/test.pdf",
        "id": "123"
    }

    with patch('app.routes.upload.supabase_service', mock_service), \
        patch('app.routes.upload.file_validator', mock_validator):

        # Créer un fichier test
        files = {
            "file": ("test.pdf", b"test content", "application/pdf")
        }

        # Faire la requête
        response = client.post("/api/upload", files=files)

        # Vérifications
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["filename"] == "test.pdf"
        assert response.json()["file_url"] == "http://test.url/test.pdf"

        # Vérifier que les mocks ont été appelés
        mock_validator.validate_file.assert_called_once()
        mock_service.upload_file.assert_called_once()

async def test_upload_validation_failure():
    # Créer un fichier invalide
    files = {
        "file": ("test.exe", b"test content", "application/x-msdownload")
    }

    # Faire la requête
    response = client.post("/api/upload", files=files)

    # Vérifications
    assert response.status_code == 400
    assert response.json()["detail"] == "Le fichier n'est pas valide"

async def test_upload_file_too_large(mock_file):
    # Préparer les mocks
    mock_validator = AsyncMock()
    mock_validator.validate_file.return_value = ValidationResult(is_valid=True)

    # Patcher la fonction upload_file pour simuler un fichier trop volumineux
    async def mock_get_size(*args, **kwargs):
        return settings.MAX_UPLOAD_SIZE + 1024  # 1KB au-dessus de la limite

    # Faire la requête avec le patch
    with patch('app.routes.upload.get_upload_file_size', mock_get_size), \
        patch('app.routes.upload.file_validator', mock_validator):

        # Créer un fichier test
        files = {
            "file": ("test.pdf", b"test content", "application/pdf")
        }

        # Faire la requête
        response = client.post("/api/upload", files=files)

        # Afficher la réponse pour le débogage
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response.json() if response.status_code != 204 else 'No content'}")

        # Vérifications
        assert response.status_code == 413
        assert response.json()["detail"] == f"Le fichier depasse la taille maximale de {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
