import pytest

from app.services.supabase_service import SupabaseService


@pytest.fixture
def supabase_service(mock_supabase):
    return SupabaseService()

async def test_upload_file_success(supabase_service, mock_supabase, mock_file):
    # Configure mock
    mock_supabase.storage.from_().upload.return_value = {"Key": "test.pdf"}
    mock_supabase.storage.from_().get_public_url.return_value = "http://test.url/test.pdf"
    mock_supabase.table().insert().execute.return_value.data = [{"id": "123"}]

    # Test
    result = await supabase_service.upload_file(mock_file)

    # Vérifications
    assert result["file_name"] == "test.pdf"
    assert result["file_url"] == "http://test.url/test.pdf"
    assert "id" in result

async def test_upload_file_failure(supabase_service, mock_supabase, mock_file):
    # Simuler une erreur
    mock_supabase.storage.from_().upload.side_effect = Exception("Upload failed")

    # Test
    with pytest.raises(Exception) as exc_info:
        await supabase_service.upload_file(mock_file)

    assert "Upload failed" in str(exc_info.value)
