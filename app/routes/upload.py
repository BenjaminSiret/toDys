"""
Routes pour la gestion des uploads de fichiers.
"""
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.file_validator import FileValidator
from ..schemas.upload import UploadResponse

router = APIRouter()
file_validator = FileValidator()

@router.post("/api/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """
    Endpoint pour l'upload de fichiers avec validation.
    
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

        # Sauvegarde du fichier
        file_path = validation_result.file_path
        content = await file.read()
        await file.seek(0)
        
        file_path.write_bytes(content)

        return UploadResponse(
            success=True,
            message="Fichier uploadé avec succès",
            filename=file_path.name,
            mime_type=validation_result.mime_type
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'upload: {str(e)}"
        )
