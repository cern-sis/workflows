import io
import os
from typing import IO

from common.repository import IRepository
from common.s3_service import S3Service


class APSRepository(IRepository):
    def __init__(self) -> None:
        super().__init__()
        self.s3_bucket = S3Service(os.getenv("APS_BUCKET_NAME", "aps"))

    def find_all(self):
        files = []
        for obj in self.s3_bucket.objects.all():
            file_name = os.path.basename(obj.key)
            files.append(file_name)
        return files

    def find_by_id(self, id: str):
        retfile = io.BytesIO()
        self.s3_bucket.download_fileobj(id, retfile)
        return retfile

    def find_the_last_uploaded_file_date(self):
        objects = list(self.s3_bucket.objects.all())
        if not objects:
            return
        dates = [obj.last_modified.strftime("%Y-%m-%d") for obj in objects]
        return max(dates)

    def save(self, key: str, obj: IO):
        self.s3_bucket.upload_fileobj(obj, key)

    def delete_all(self):
        self.s3_bucket.objects.all().delete()
