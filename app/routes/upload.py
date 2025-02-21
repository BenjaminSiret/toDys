"""
Routes pour la gestion des uploads de fichiers.
"""
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..schemas.upload import UploadResponse
from ..services.file_validator import FileValidator
from ..services.supabase_service import SupabaseService

router = APIRouter()
file_validator = FileValidator()
supabase_service = SupabaseService()

@router.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """
    Endpoint pour l'upload de fichiers avec validation et stockage dans Supabase.

    Args:
        file: Le fichier à uploader

    Returns:
        UploadResponse: Résultat de l'opération

    Raises:
        HTTPException: En cas d'erreur lors de l'upload
    """
    try:
        # Validation du fichier
        validation_result = await file_validator.validate_file(file)

        if not validation_result.is_valid:
            return UploadResponse(
                success=False,
                message="Échec de la validation",
                error=validation_result.error_message
            )

        # Upload vers Supabase
        try:
            upload_result = await supabase_service.upload_file(file)

            return UploadResponse(
                success=True,
                message="Fichier uploadé avec succès",
                filename=upload_result['file_name'],
                file_url=upload_result['file_url'],
                mime_type=file.content_type
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de l'upload vers Supabase: {str(e)}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement du fichier: {str(e)}"
        )
