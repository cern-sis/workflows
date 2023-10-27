import io
from os import listdir

from common.pull_ftp import migrate_files
from common.repository import IRepository
from elsevier.repository import ElsevierRepository
from elsevier.sftp_service import ElsevierSFTPService
from pytest import fixture
from structlog import get_logger


@fixture
def elsevier_empty_repo(shared_datadir):
    repo = ElsevierRepository()
    repo.delete_all()
    yield repo


def test_migrate_files(elsevier_empty_repo):
    archives_names = ["CERNQ000000010011A.tar", "CERNQ000000010669A.tar", "empty.xml"]
    with ElsevierSFTPService() as sftp:
        extracted_filenames = migrate_files(
            archives_names, sftp, elsevier_empty_repo, logger=get_logger()
        )
        assert extracted_filenames == [
            "extracted/CERNQ000000010011A/CERNQ000000010011/dataset.xml",
            "extracted/CERNQ000000010011A/CERNQ000000010011/S0550321323000354/main.xml",
            "extracted/CERNQ000000010011A/CERNQ000000010011/S0550321323000366/main.xml",
            "extracted/CERNQ000000010011A/CERNQ000000010011/S0370269323000643/main.xml",
            "extracted/CERNQ000000010011A/CERNQ000000010011/S0370269323000850/main.xml",
            "extracted/CERNQ000000010669A/CERNQ000000010669/dataset.xml",
            "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005105/main.xml",
            "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005075/main.xml",
            "extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323005099/main.xml",
        ]
