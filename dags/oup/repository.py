import os
from io import BytesIO
from typing import IO

from common.repository import IRepository
from common.s3_service import S3Service


class OUPRepository(IRepository):
    ZIPED_DIR: str = "raw/"
    EXTRACTED_DIR: str = "extracted/"

    def __init__(self) -> None:
        super().__init__()
        self.s3 = S3Service(os.getenv("OUP_BUCKET_NAME", "oup"))

    def get_all_raw_filenames(self):
        return [
            os.path.basename(f.key)
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
            file_name = os.path.basename(file)
            filename_without_extension = file_name.split(".")[0]
            if filename_without_extension not in ret_dict.keys():
                ret_dict[filename_without_extension] = dict()
            ret_dict[filename_without_extension][
                "xml" if self.is_meta(file_name) else "pdf"
            ] = file
        return list(ret_dict.values())

    def find_by_id(self, id: str):
        retfile = BytesIO()
        self.s3.download_fileobj(id, retfile)
        return retfile

    def save(self, filename: str, obj: IO):
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

    def is_meta(self, filename: str):
        return ".xml" in filename
