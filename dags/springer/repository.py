import os
from io import BytesIO

from common.repository import IRepository
from common.s3_service import S3Service
from structlog import get_logger

logger = get_logger()


class SpringerRepository(IRepository):
    ZIPED_DIR = "raw/"
    EXTRACTED_DIR = "extracted/"

    def __init__(self) -> None:
        super().__init__()
        self.bucket = os.getenv("SPRINGER_BUCKET_NAME", "springer")
        self.s3 = S3Service(self.bucket)

    def get_all_raw_filenames(self):
        return [
            f.key.replace("raw/", "")
            for f in self.s3.objects.filter(Prefix=self.ZIPED_DIR).all()
        ]

    def find_all(self, filenames_to_process=None):
        ret_dict = {}
        filenames = []
        filenames = (
            filenames_to_process
            if filenames_to_process
            else self.__find_all_extracted_files()
        )
        for file in filenames:
            file_parts = file.split("/")
            last_part = file_parts[-1]
            filename_without_extension = last_part.split(".")[0]
            if filename_without_extension not in ret_dict.keys():
                ret_dict[filename_without_extension] = dict()
            ret_dict[filename_without_extension][
                "xml" if self.is_meta(last_part) else "pdf"
            ] = file
        return list(ret_dict.values())

    def get_by_id(self, id):
        retfile = BytesIO()
        self.s3.download_fileobj(id, retfile)
        return retfile

    def save(self, filename, obj):
        prefix = self.ZIPED_DIR if ".zip" in filename else self.EXTRACTED_DIR
        self.s3.upload_fileobj(obj, prefix + filename)

    def delete_all(self):
        self.s3.objects.all().delete()

    def __find_all_extracted_files(self):
        return [
            f.key
            for f in self.s3.objects.filter(Prefix=self.EXTRACTED_DIR).all()
            if self.is_meta(f.key) or ".pdf" in f.key
        ]

    def is_meta(self, filename):
        return ".Meta" in filename or ".scoap" in filename
