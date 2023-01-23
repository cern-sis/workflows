import base64
import io
import zipfile
from datetime import datetime
from typing import Dict

from airflow.api.common import trigger_dag
from common.repository import IRepository
from common.sftp_service import SFTPService
from structlog import PrintLogger


def migrate_files(filenames, sftp: SFTPService, repo: IRepository, logger: PrintLogger):
    logger.msg("Processing files.", filenames=filenames)
    extracted_filenames = []
    for _file in filenames:
        logger.msg("Getting file from SFTP.", file=_file)
        file_bytes = sftp.get_file(_file)
        if not zipfile.is_zipfile(file_bytes):
            logger.msg("File is not a zipfile, processing next file.")
            continue
        with zipfile.ZipFile(file_bytes) as zip:
            for zip_filename in zip.namelist():
                file_prefix = _file.split(".")[0]
                file_content = zip.read(zip_filename)
                s3_filename = file_prefix + "/" + zip_filename
                repo.save(s3_filename, io.BytesIO(file_content))
                if repo.is_meta(s3_filename):
                    extracted_filenames.append("extracted/" + s3_filename)
        repo.save(_file, file_bytes)
    return extracted_filenames


def migrate_from_ftp(
    sftp: SFTPService, repo: IRepository, logger: PrintLogger, **kwargs
):
    params = kwargs["params"]
    if "force_pull" in params and params["force_pull"]:
        return _force_pull(sftp, repo, logger)
    elif "filenames_pull" in params and params["filenames_pull"]["enabled"]:
        return _filenames_pull(params["filenames_pull"], sftp, repo, logger)
    return _differential_pull(sftp, repo, logger)


def _force_pull(sftp: SFTPService, repo: IRepository, logger: PrintLogger):
    logger.msg("Force Pulling from SFTP.")
    filenames = sftp.list_files()
    return migrate_files(filenames, sftp, repo, logger)


def _filenames_pull(
    filenames_pull_params: Dict,
    sftp: SFTPService,
    repo: IRepository,
    logger: PrintLogger,
):
    filenames = filenames_pull_params["filenames"]
    force_from_ftp = filenames_pull_params["force_from_ftp"]
    if force_from_ftp:
        logger.msg("Pulling specified filenames from SFTP", filenames=filenames)
        return migrate_files(filenames, sftp, repo, logger)
    logger.msg("Processing specified filenames.", filenames=filenames)
    return _find_files_in_zip(filenames, repo)


def _find_files_in_zip(filenames, repo: IRepository):
    extracted_filenames = []
    for zipped_filename in filenames:
        zipped_file: str = repo.find_by_id(f"raw/{zipped_filename}")
        with zipfile.ZipFile(zipped_file) as zip:
            for zip_filename in zip.namelist():
                if repo.is_meta(zip_filename):
                    filename_without_extension = filenames[0].split(".")[0]
                    extracted_filenames.append(
                        f"extracted/{filename_without_extension}/{zip_filename}"
                    )
    return extracted_filenames


def _differential_pull(sftp: SFTPService, repo: IRepository, logger: PrintLogger):
    logger.msg("Pulling missing files only.")
    sftp_files = sftp.list_files()
    s3_files = repo.get_all_raw_filenames()
    diff_files = list(filter(lambda x: x not in s3_files, sftp_files))
    return migrate_files(diff_files, sftp, repo, logger)


def trigger_file_processing(
    publisher: str,
    repo: IRepository,
    logger: PrintLogger,
    filenames=None,
    article_splitter_function=lambda x: [x],
):
    files = []
    if filenames is not None:
        files = filenames
    else:
        files = list(map(lambda x: x["xml"], repo.find_all()))
    for filename in files:
        logger.msg("Running processing.", filename=filename)
        file_bytes = repo.find_by_id(filename)

        for article in article_splitter_function(file_bytes):
            _id = _generate_id(publisher)
            encoded_article = base64.b64encode(article.getvalue()).decode()
            trigger_dag.trigger_dag(
                dag_id=f"{publisher}_process_file",
                run_id=_id,
                conf={"file": encoded_article},
                replace_microseconds=False,
            )
    return files


def _generate_id(publisher: str):
    return datetime.utcnow().strftime(f"{publisher}_%Y-%m-%dT%H:%M:%S.%f")
