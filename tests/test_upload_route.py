import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.file_validator import ValidationResult
from app.services.supabase_service import SupabaseService

client = TestClient(app)

@pytest.mark.asyncio
async def test_upload_success(mock_file, mock_supabase):from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.file_validator import ValidationResult
from app.services.supabase_service import SupabaseService

client = TestClient(app)

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

def test_upload_validation_failure():
    # Créer un fichier invalide
    files = {
        "file": ("test.exe", b"test content", "application/x-msdownload")
    }

    # Faire la requête
    response = client.post("/api/upload", files=files)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "validation" in response.json()["message"].lower()
    # Préparer les mocks
    mock_validator = AsyncMock()
    mock_validator.validate_file.return_value = ValidationResult(is_valid=True)

    mock_service = AsyncMock(spec=SupabaseService)
    mock_service.upload_file.return_value = {
        "file_name": "test.pdf",
        "file_url": "http://test.url/test.pdf",
        "id": "123"
    }

    with patch('app.routes.upload.supabase_service', return_value=mock_service), \
        patch('app.routes.upload.file_validator', return_value=mock_validator):
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

def test_upload_validation_failure(mock_file):
    # Créer un fichier invalide
    files = {
        "file": ("test.exe", b"test content", "application/x-msdownload")
    }

    # Faire la requête
    response = client.post("/api/upload", files=files)

    # Vérifications
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert "validation" in response.json()["message"].lower()
