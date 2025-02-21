from unittest.mock import Mock, patch
import asyncio

import pytest
from fastapi import UploadFile


@pytest.fixture
def mock_file():
    """Fixture pour simuler un fichier uploadé."""
    file = Mock(spec=UploadFile)
    file.filename = "test.pdf"
    file.content_type = "application/pdf"
    
    async def async_read():
        return b"test content"
    
    async def async_seek(position):
        pass
    
    file.read = async_read
    file.seek = async_seek
    return file

@pytest.fixture
def mock_supabase():
    """Fixture pour simuler le client Supabase."""
    with patch('app.services.supabase_service.create_client') as mock_create:
        mock_client = Mock()
        mock_create.return_value = mock_client
        yield mock_client
