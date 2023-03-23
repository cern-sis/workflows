from common.pull_ftp import migrate_from_ftp
from iop.repository import IOPRepository
from iop.sftp_service import IOPSFTPService
from pytest import fixture
from structlog import get_logger


@fixture
def iop_empty_repo():
    repo = IOPRepository()
    repo.delete_all()
    yield repo


def test_pull_from_sftp(iop_empty_repo):
    with IOPSFTPService() as sftp:
        migrate_from_ftp(
            sftp,
            iop_empty_repo,
            get_logger().bind(class_name="test_logger"),
            **{
                "params": {
                    "force_pull": False,
                    "excluded_directories": [],
                    "filenames_pull": {
                        "enabled": False,
                        "filenames": [],
                        "force_from_ftp": False,
                    },
                }
            }
        )
        expected_files = [
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085001/cpc_46_8_085001.xml",
            },
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085104/cpc_46_8_085104.xml",
            },
            {
                "pdf": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.pdf",
                "xml": "extracted/2022-07-30T03_02_01_content/1674-1137/1674-1137_46/1674-1137_46_8/1674-1137_46_8_085106/cpc_46_8_085106.xml",
            },
            {
                "pdf": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.pdf",
                "xml": "extracted/2022-09-01T03_01_40_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093111/cpc_46_9_093111.xml",
            },
            {
                "pdf": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.pdf",
                "xml": "extracted/2022-09-03T03_01_49_content/1674-1137/1674-1137_46/1674-1137_46_9/1674-1137_46_9_093110/cpc_46_9_093110.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103001/cpc_46_10_103001.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103101/cpc_46_10_103101.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103102/cpc_46_10_103102.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103104/cpc_46_10_103104.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103105/cpc_46_10_103105.xml",
            },
            {
                "pdf": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.pdf",
                "xml": "extracted/2022-09-24T03_01_43_content/1674-1137/1674-1137_46/1674-1137_46_10/1674-1137_46_10_103108/cpc_46_10_103108.xml",
            },
            {"xml": "extracted/aca95c/aca95c.xml"},
        ]
        assert iop_empty_repo.find_all() == expected_files
        assert sorted(iop_empty_repo.get_all_raw_filenames()) == sorted(
            [
                "2022-07-30T03_02_01_content.zip",
                "2022-09-01T03_01_40_content.zip",
                "2022-09-03T03_01_49_content.zip",
                "2022-09-24T03_01_43_content.zip",
                "aca95c.xml.zip",
            ]
        )
