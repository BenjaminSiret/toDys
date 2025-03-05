"""
Routes pour la gestion des uploads de fichiers.
"""
import logging
import traceback
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..config import get_settings
from ..schemas.upload import UploadResponse
from ..services.file_validator import FileValidator
from ..services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)

router = APIRouter()
file_validator = FileValidator()
supabase_service = SupabaseService()
settings = get_settings()

async def get_upload_file_size(file: UploadFile) -> Optional[int]:
  try:
    return len(await file.read())
  except Exception as e:
    raise ValueError(f"Erreur lors de la lecture du fichier: {str(e)}")
  finally:
    await file.seek(0)

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
        # Vérification de la taille du fichier
        file_size = await get_upload_file_size(file)
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Le fichier depasse la taille maximale de {}MB".format(settings.MAX_UPLOAD_SIZE / 1024 / 1024)
            )

        # Validation du fichier
        validation_result = await file_validator.validate_file(file)

        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400,
                detail="Le fichier n'est pas valide"
            )

        # Upload vers Supabase
        upload_result = await supabase_service.upload_file(file)

        return UploadResponse(
            success=True,
            message="Fichier uploadé avec succès",
            filename=upload_result['file_name'],
            file_url=upload_result['file_url'],
            mime_type=file.content_type
        )

    except HTTPException as e:
        logger.error(
            f"HTTP Exception interceptée",
            extra={
                "status_code": e.status_code,
                "error_detail": e.detail,
                "file_name": file.filename,
                "traceback": traceback.format_exc()
            }
        )
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement du fichier: {str(e)}"
        )
