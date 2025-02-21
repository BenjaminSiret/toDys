"""
Service pour gérer les interactions avec Supabase.
"""
import os
from datetime import datetime
from typing import Any, Dict

from fastapi import UploadFile
from supabase import Client, create_client


class SupabaseService:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.bucket_name = "temp-files"

    async def upload_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Upload un fichier vers Supabase et crée un enregistrement dans la base.

        Args:
            file: Le fichier à uploader

        Returns:
            Dict contenant les informations du fichier uploadé
        """
        try:
            # Créer le chemin du fichier avec la date
            today = datetime.now().strftime('%Y%m%d')
            file_path = f"{today}/{file.filename}"

            # Lire le contenu du fichier
            content = await file.read()
            await file.seek(0)  # Remettre le curseur au début

            # Upload vers Supabase Storage
            self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                content
            )

            # Créer l'enregistrement dans la base
            file_record = self.supabase.table('temp_files').insert({
                'file_name': file.filename,
                'file_type': file.content_type,
                'original_file_path': file_path,
                'status': 'uploaded'
            }).execute()

            # Obtenir l'URL publique
            file_url = self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)

            return {
                'id': file_record.data[0]['id'],
                'file_name': file.filename,
                'file_url': file_url
            }

        except Exception as e:
            raise Exception(f"Erreur lors de l'upload: {str(e)}")

    async def update_file_status(self, file_id: str, status: str, transformed_path: str = None) -> Dict[str, Any]:
        """
        Met à jour le statut d'un fichier.
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
