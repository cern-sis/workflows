import base64
import io
import tarfile
import zipfile
from datetime import datetime

from airflow.api.common import trigger_dag
from common.ftp_service import FTPService
from common.repository import IRepository
from common.sftp_service import SFTPService
from common.utils import process_archive
from structlog import PrintLogger

SFTP_FTP_TYPE = (FTPService, SFTPService)


def migrate_files(
    archives_names,
    s_ftp: SFTP_FTP_TYPE,
    repo: IRepository,
    excluded_extensions: list,
    logger: PrintLogger,
):
    logger.msg("Processing files.", filenames=archives_names)
    extracted_filenames = []
    extracted_xml_filenames = []

    for excluded_extension in excluded_extensions:
        for index, archive_name in enumerate(archives_names):
            if excluded_extension in archive_name:
                archives_names.pop(index)

    for archive_name in archives_names:
        logger.msg("Getting file from SFTP.", file=archive_name)
        file_bytes = s_ftp.get_file(archive_name)

        if (
            ".zip" in archive_name
            and zipfile.is_zipfile(file_bytes)
            or ".tar" in archive_name
            and tarfile.is_tarfile(file_bytes)
        ):
            for (archive_file_content, s3_filename) in process_archive(
                file_bytes=file_bytes, file_name=archive_name
            ):
                repo.save(s3_filename, io.BytesIO(archive_file_content))
                if repo.is_meta(s3_filename):
                    extracted_filenames.append("extracted/" + s3_filename)
                    if ".xml" in s3_filename:
                        extracted_xml_filenames.append("extracted/" + s3_filename)
            repo.save(archive_name, file_bytes)

        else:
            logger.info(
                "File is not zip or tar, processing the next one",
                file_name=archive_name,
            )
            continue
    logger.info("Extracted files ", extracted_filenames=extracted_filenames)
    logger.info(
        "Files parsed for parser", extracted_xml_filenames=extracted_xml_filenames
    )

    return extracted_xml_filenames


def migrate_from_ftp(
    s_ftp: SFTP_FTP_TYPE, repo: IRepository, logger: PrintLogger, **kwargs
):
    params = kwargs["params"]
    force_pull_specific_files = (
        "filenames_pull" in params
        and params["filenames_pull"]["enabled"]
        and params["filenames_pull"]["force_from_ftp"]
    )
    force_pull_all_files = (
        "filenames_pull" in params
        and not params["filenames_pull"]["enabled"]
        and params["force_pull"]
    )

    if force_pull_all_files:
        return _force_pull(s_ftp, repo, logger, **kwargs)
    elif force_pull_specific_files:
        return _filenames_pull(s_ftp, repo, logger, **kwargs)
    return _differential_pull(s_ftp, repo, logger, **kwargs)


def reprocess_files(repo: IRepository, logger: PrintLogger, **kwargs):
    logger.msg("Processing specified filenames.")
    filenames_pull_params = kwargs["params"]["filenames_pull"]
    filenames = filenames_pull_params["filenames"]
    return _find_files_in_zip(filenames, repo)


def _force_pull(s_ftp: SFTP_FTP_TYPE, repo: IRepository, logger: PrintLogger, **kwargs):
    logger.msg("Force Pulling from SFTP.")
    excluded_directories = kwargs["params"]["excluded_directories"]
    filenames = s_ftp.list_files(excluded_directories=excluded_directories)
    excluded_extensions = kwargs["params"]["excluded_extensions"]
    return migrate_files(filenames, s_ftp, repo, excluded_extensions, logger)


def _filenames_pull(
    s_ftp: SFTP_FTP_TYPE,
    repo: IRepository,
    logger: PrintLogger,
    **kwargs,
):
    filenames_pull_params = kwargs["params"]["filenames_pull"]
    filenames = filenames_pull_params["filenames"]
    logger.msg("Pulling specified filenames from SFTP")
    excluded_extensions = kwargs["params"]["excluded_extensions"]
    return migrate_files(filenames, s_ftp, repo, excluded_extensions, logger)


def _find_files_in_zip(filenames, repo: IRepository):
    extracted_filenames = []
    for zipped_filename in filenames:
        zipped_file: str = repo.get_by_id(f"raw/{zipped_filename}")
        with zipfile.ZipFile(zipped_file) as zip:
            for zip_filename in zip.namelist():
                if repo.is_meta(zip_filename):
                    filename_without_extension = zipped_filename.split(".")[0]
                    extracted_filenames.append(
                        f"extracted/{filename_without_extension}/{zip_filename}"
                    )
    return extracted_filenames


def _differential_pull(
    s_ftp: SFTP_FTP_TYPE, repo: IRepository, logger: PrintLogger, **kwargs
):
    logger.msg("Pulling missing files only.")
    excluded_directories = kwargs["params"]["excluded_directories"]
    sftp_files = s_ftp.list_files(excluded_directories=excluded_directories)
    s3_files = repo.get_all_raw_filenames()
    diff_files = list(filter(lambda x: x not in s3_files, sftp_files))
    excluded_extensions = kwargs["params"]["excluded_extensions"]
    return migrate_files(diff_files, s_ftp, repo, excluded_extensions, logger)


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
        file_bytes = repo.get_by_id(filename)

        for article in article_splitter_function(file_bytes):
            _id = _generate_id(publisher)
            encoded_article = base64.b64encode(article.getvalue()).decode()
            trigger_dag.trigger_dag(
                dag_id=f"{publisher}_process_file",
                run_id=_id,
                conf={"file": encoded_article, "file_name": filename},
                replace_microseconds=False,
            )
    return files


def _generate_id(publisher: str):
    return datetime.utcnow().strftime(f"{publisher}_%Y-%m-%dT%H:%M:%S.%f")
