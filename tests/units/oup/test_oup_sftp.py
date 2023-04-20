from oup.sftp_service import OUPSFTPService


def test_oup_sftp_path():
    with OUPSFTPService() as sftp:
        files = sftp.list_files()
    assert sorted(files) == sorted(
        [
            "2022-09-22_00:30:02_ptep_iss_2022_9.img.zip",
            "2022-09-22_00:30:02_ptep_iss_2022_9.pdf.zip",
            "2022-09-22_00:30:02_ptep_iss_2022_9.xml.zip",
            "2022-09-22_00:30:02_ptep_iss_2022_9_archival.zip",
        ]
    )
