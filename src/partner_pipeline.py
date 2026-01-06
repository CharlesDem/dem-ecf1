from datetime import date
import hashlib
from io import BytesIO
import json
import time
from typing import Optional

import pandas as pd
import structlog
from src.db.queries import save_partners
from src.coordinates_helper import get_cordinates_from_address
from src.models.models import Partner
from src.minio_client import DataType, MinIOStorage

logger = structlog.get_logger()

class PartnerPipeline:


    def __hash_data(self, value: str) -> str:
        if value is None:
            return None
        return hashlib.sha256(value.encode("utf-8")).hexdigest()   

    def __get_partners(self, bucket: str, filename: str) -> Optional[list[Partner]]:
        minio_client = MinIOStorage()

        data = minio_client.get_object(bucket, filename)
        if data is None:
            return None

        df = pd.read_excel(BytesIO(data))

        partners = [
            Partner(
                book_store_name=p["nom_librairie"],
                address=p["adresse"],
                zipcode=p["code_postal"],
                city=p["ville"],
                longitude = None,
                latitude = None,
                name=self.__hash_data(p["contact_nom"]), #TODO être sûr que ça apparait jamais dans les logs
                email=self.__hash_data(p["contact_email"]),
                phone=self.__hash_data(str(p["contact_telephone"])),
                revenue=float(p["ca_annuel"]),
                partner_date=date.fromisoformat(p["date_partenariat"]),
                speciality=p["specialite"],
            )
            for p in df.to_dict(orient="records")
        ]

        return partners
    
    def __get_coordinates(self, address: str):
        return get_cordinates_from_address(address)
    
    def save_partners(self):
        partners = self.__get_partners("client", "partenaire_librairies.xlsx")

        if not partners:
            logger.error("No data found")
            return

        for p in partners:
            longitude, latitude = self.__get_coordinates(p.address)
            p.longitude = longitude
            p.latitude = latitude
            time.sleep(2)

        save_partners(partners)


        
def main():
    partner_pipeline = PartnerPipeline()
    partner_pipeline.save_partners()

if __name__=="__main__":
    main()


