"""
Service pour gérer les interactions avec Supabase.
"""
import os
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import UploadFile
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)
        self.bucket_name = "temp_files"

    async def upload_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Upload un fichier vers Supabase et crée un enregistrement dans la base.

        Args:
            file (UploadFile): Le fichier à uploader
        
        Returns:
            Dict[str, Any]: Informations sur le fichier uploadé incluant URL et ID en base
        """
        try:
            # Lire le contenu du fichier
            content = await file.read()
            
            # Upload vers Supabase Storage
            file_path = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            upload_response = self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                content
            )

            # Obtenir l'URL publique
            file_url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)

            # Créer l'enregistrement dans la base de données
            expires_at = datetime.now() + timedelta(days=1)
            db_response = self.supabase.table("temp_files").insert({
                "file_name": file.filename,
                "file_type": file.content_type,
                "original_file_path": file_path,
                "status": "uploaded",
                "expires_at": expires_at.isoformat()
            }).execute()

            # Réinitialiser le curseur du fichier pour une utilisation ultérieure
            await file.seek(0)

            return {
                "id": db_response.data[0]["id"],
                "file_name": file.filename,
                "file_url": file_url
            }

        except Exception as e:
            # En cas d'erreur, propager l'exception
            raise Exception(f"Erreur lors de l'upload: {str(e)}")

    async def update_file_status(self, file_id: str, status: str, transformed_path: str = None) -> Dict[str, Any]:
        """
        Met à jour le statut d'un fichier.
        
        Args:
            file_id (str): L'identifiant du fichier à mettre à jour
            status (str): Le nouveau statut du fichier
            transformed_path (str, optional): Le chemin du fichier transformé, si applicable
            
        Returns:
            Dict[str, Any]: Les données mises à jour du fichier
        """
        update_data = {
            'status': status,
            'processed_at': datetime.now().isoformat()
        }

        if transformed_path:
            update_data['transformed_file_path'] = transformed_path

        result = self.supabase.table('temp_files')\
            .update(update_data)\
            .eq('id', file_id)\
            .execute()

        return result.data[0] if result.data else None
