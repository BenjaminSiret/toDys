from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_upload_success(mock_file, mock_supabase):
    # Préparer le mock
    with patch('app.routes.upload.supabase_service') as mock_service:
        mock_service.upload_file.return_value = {
            "file_name": "test.pdf",
            "file_url": "http://test.url/test.pdf",
            "id": "123"
        }

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
