from iop.sftp_service import IOPSFTPService


def test_iop_sftp_path():
    files = []
    with IOPSFTPService() as sftp:
        files = sftp.list_files()
    assert files == [
        "2022-07-30T03_02_01_content.zip",
        "2022-09-01T03_01_40_content.zip",
        "2022-09-03T03_01_49_content.zip",
        "2022-09-24T03_01_43_content.zip",
    ]
