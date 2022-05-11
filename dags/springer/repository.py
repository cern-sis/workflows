import os
from io import BytesIO
from typing import IO

from common.repository import IRepository
from common.s3_service import S3Service


class SpringerRepository(IRepository):
    ZIPED_DIR: str = "raw/"
    EXTRACTED_DIR: str = "extracted/"

    def __init__(self) -> None:
        super().__init__()
        self.s3 = S3Service(os.getenv("SPRINGER_REPO_BUCKET", "springer"))

    def find_all(self):
        ret_dict = {}
        filenames = self.__find_all_extracted_files()
        for file in filenames:
            file_parts = file.split("/")
            last_part = file_parts[-1]
            filename_without_extension = last_part.split(".")[0]
            if filename_without_extension not in ret_dict.keys():
                ret_dict[filename_without_extension] = dict()
            ret_dict[filename_without_extension][
                "xml" if self.__file_is_meta(last_part) else "pdf"
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
            if self.__file_is_meta(f.key) or ".pdf" in f.key
        ]

    def __file_is_meta(self, filename: str):
        return ".Meta" in filename or ".scoap" in filename
