import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import UploadFile

load_dotenv()

class SupabaseService:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)
        self.bucket_name = "temp_files"

    async def upload_file(self, file: UploadFile) -> dict:
        """
        Upload a file to Supabase storage and create a database record.
        
        Args:
            file (UploadFile): The file to upload
        
        Returns:
            dict: Information about the uploaded file including URL and database ID
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
