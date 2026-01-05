from enum import Enum
import io
from typing import Optional
from minio import Minio
from minio.error import S3Error
import structlog
from src.config.minio_config import minio_config
from minio.versioningconfig import VersioningConfig

logger = structlog.get_logger()

class DataType(Enum):
    QUOTE= "quote"
    BOOK= "book"
    CLIENT = "client"

bucket_upload = {
    DataType.QUOTE : {
        "bucket": minio_config.bucket_quotes,
        "content_type": "text/json"
    },
    DataType.CLIENT : {
        "bucket": minio_config.bucket_clients,
        "content_type": "text/xlsxl"
    },
    DataType.BOOK: {
        "bucket": minio_config.bucket_books,
        "content_type": "text/json"
    }
}
    

class MinIOStorage:

    def __init__(self):
        self.client = Minio(
            endpoint=minio_config.endpoint,
            access_key=minio_config.access_key,
            secret_key=minio_config.secret_key,
            secure=minio_config.secure
        )
        self._ensure_buckets()
    
    def _ensure_buckets(self) -> None:

        buckets = [
            minio_config.bucket_books,
            minio_config.bucket_clients,
            minio_config.bucket_quotes
        ]

        for bucket in buckets:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)
                versioning_config = VersioningConfig(status="Enabled")
                self.client.set_bucket_versioning(bucket_name=bucket, config=versioning_config) #on veut les versions du scrap


    def upload(self, data_type: DataType, filename: str, data_bytes):
        try:
            result = self.client.put_object(
                bucket_name= bucket_upload[data_type]["bucket"],
                object_name=filename,
                data=io.BytesIO(data_bytes),
                length=len(data_bytes),
                content_type=bucket_upload[data_type]["content_type"]
            )

            version_id = getattr(result, "version_id", None)
            
            return {
                        "url": f"minio://{minio_config.bucket_quotes}/{filename}",
                        "version": version_id
            }
            
        except S3Error as e:
            logger.error("image_upload_failed", error=str(e))
            return None

    
    def get_object(self, bucket: str, filename: str) -> Optional[bytes]:
        """Télécharge un objet."""
        try:
            response = self.client.get_object(bucket, filename)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error:
            return None
    
    def list_objects(self, bucket: str, prefix: str = "") -> list[dict]:
        """Liste les objets d'un bucket."""
        objects = self.client.list_objects(bucket, prefix=prefix, recursive=True)
        return [
            {
                "name": obj.object_name,
                "size": obj.size,
                "modified": obj.last_modified
            }
            for obj in objects
        ]
    
    def delete_object(self, bucket: str, filename: str) -> bool:
        """Supprime un objet."""
        try:
            self.client.remove_object(bucket, filename)
            return True
        except S3Error:
            return False
    
    def get_presigned_url(
        self,
        bucket: str,
        filename: str,
        expires_hours: int = 24
    ) -> Optional[str]:
        """Génère une URL temporaire."""
        from datetime import timedelta
        try:
            return self.client.presigned_get_object(
                bucket_name=bucket,
                object_name=filename,
                expires=timedelta(hours=expires_hours)
            )
        except S3Error:
            return None