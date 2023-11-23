from common.pull_ftp import migrate_files
from elsevier.repository import ElsevierRepository
from elsevier.sftp_service import ElsevierSFTPService
from elsevier.trigger_file_processing import trigger_file_processing_elsevier
from pytest import fixture
from structlog import get_logger


@fixture
def elsevier_sftp():
    return ElsevierSFTPService()


@fixture
def elsevier_empty_repo():
    repo = ElsevierRepository()
    repo.delete_all()
    yield repo


@fixture
def logger():
    return get_logger().bind(class_name="elsevier_pull_ftp")


@fixture
def migrated_files(elsevier_empty_repo, elsevier_sftp, logger):
    with elsevier_sftp as sftp:
        return migrate_files(
            ["CERNQ000000010011A.tar", "vtex00403986_a-2b_CLEANED.zip"],
            sftp,
            elsevier_empty_repo,
            logger,
            process_archives=False,
        )


def test_trigger_file_processing_elsevier(elsevier_empty_repo, migrated_files):
    files = trigger_file_processing_elsevier(
        publisher="elsevier",
        repo=elsevier_empty_repo,
        logger=get_logger().bind(class_name="elsevier_pull_ftp"),
        filenames=migrated_files,
    )
    assert sorted(files) == sorted(
        [
            "CERNQ000000010011/S0550321323000354/main.xml",
            "CERNQ000000010011/S0550321323000366/main.xml",
            "CERNQ000000010011/S0370269323000643/main.xml",
            "CERNQ000000010011/S0370269323000850/main.xml",
            "vtex00403986_a-2b_CLEANED/03702693/v791sC/S0370269319301078/main.xml",
        ]
    )
