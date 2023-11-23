import base64
import io
import os

from airflow.api.common import trigger_dag
from common.pull_ftp import _generate_id
from common.repository import IRepository
from common.utils import parse_without_names_spaces, process_archive
from elsevier.metadata_parser import ElsevierMetadataParser
from structlog import PrintLogger


def trigger_file_processing_elsevier(
    publisher: str,
    repo: IRepository,
    logger: PrintLogger,
    filenames=None,
):
    files = []
    for filename in filenames:
        logger.msg("Running processing.", filename=filename)
        file_bytes = repo.get_by_id(filename)
        (archive_file_content, s3_filename) = next(
            process_archive(
                file_bytes=file_bytes,
                file_name=filename,
                only_specific_file="dataset.xml",
            )
        )
        dataset_file = parse_without_names_spaces(archive_file_content.decode("utf-8"))
        parser = ElsevierMetadataParser(file_path=filename)
        parsed_articles = parser.parse(dataset_file)
        for parsed_article in parsed_articles:
            full_file_path = parsed_article["files"]["xml"]
            (file_content, _) = next(
                process_archive(
                    file_bytes=file_bytes,
                    file_name=s3_filename,
                    only_specific_file=full_file_path,
                )
            )

            repo.save(full_file_path, io.BytesIO(file_content))
            logger.msg("Running processing.", filename=full_file_path)

            file_bytes_extracted = repo.get_by_id(
                os.path.join(*["extracted", full_file_path])
            )
            _id = _generate_id(publisher)
            encoded_article = base64.b64encode(file_bytes_extracted.getvalue()).decode()
            trigger_dag.trigger_dag(
                dag_id=f"{publisher}_process_file",
                run_id=_id,
                conf={
                    "file_content": encoded_article,
                    "file_name": full_file_path,
                    "metadata": parsed_article,
                },
                replace_microseconds=False,
            )
            files.append(full_file_path)
    return files
