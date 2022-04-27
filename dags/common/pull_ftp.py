import base64
import io
import zipfile
from datetime import datetime

from airflow.api.common import trigger_dag
from common.repository import IRepository
from common.sftp_service import SFTPService


def migrate_from_ftp(sftp: SFTPService, repo: IRepository):
    filenames = sftp.list_files()
    for file in filenames:
        file_bytes = sftp.get_file(file)
        with zipfile.ZipFile(file_bytes) as zip:
            for zip_filename in zip.namelist():
                file_prefix = file.split(".")[0]
                file_content = zip.read(zip_filename)
                repo.save(file_prefix + "/" + zip_filename, io.BytesIO(file_content))
        repo.save(file, file_bytes)


def trigger_file_processing(
    publisher: str, repo: IRepository, article_splitter_function=lambda x: [x]
):
    files = repo.find_all()
    for filenames in files:
        file_bytes = repo.find_by_id(filenames["xml"])

        for article in article_splitter_function(file_bytes):
            id = _generate_id(publisher)
            encoded_article = base64.b64encode(article.getvalue()).decode()
            trigger_dag.trigger_dag(
                dag_id=f"{publisher}_process_file",
                run_id=id,
                conf={"file": encoded_article},
                replace_microseconds=False,
            )
    return files


def _generate_id(publisher: str):
    return datetime.utcnow().strftime(f"{publisher}_%Y-%m-%dT%H:%M:%S.%f")
