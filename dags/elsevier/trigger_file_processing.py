import os

from airflow.api.common import trigger_dag
from common.pull_ftp import _generate_id
from common.utils import parse_without_names_spaces
from elsevier.metadata_parser import ElsevierMetadataParser
from structlog import get_logger

logger = get_logger()


def trigger_file_processing_elsevier(
    publisher,
    repo,
    logger,
    filenames=None,
):
    files = []
    for filename in filenames:
        if "dataset.xml" != os.path.basename(filename):
            continue
        logger.msg("Running processing.", filename=filename)
        file_bytes = repo.get_by_id(filename)

        dataset_file = parse_without_names_spaces(file_bytes)
        parser = ElsevierMetadataParser(file_path=filename)
        parsed_articles = parser.parse(dataset_file)
        for parsed_article in parsed_articles:
            full_file_path = parsed_article["files"]["xml"]
            logger.msg("Processing file", file=full_file_path)
            _id = _generate_id(publisher)
            trigger_dag.trigger_dag(
                dag_id=f"{publisher}_process_file",
                run_id=_id,
                conf={
                    "file_name": full_file_path,
                    "metadata": parsed_article,
                },
                replace_microseconds=False,
            )
            files.append(full_file_path)
    return files
