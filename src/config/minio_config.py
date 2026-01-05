import os
from dataclasses import dataclass

@dataclass
class MinIOConfig:
    endpoint: str = os.getenv("S3_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    secure: bool = os.getenv("S3_SECURE", "false").lower() == "true"
    bucket_quotes:str = "quotes"
    bucket_clients:str = "client"
    bucket_books:str = "books"


minio_config = MinIOConfig()