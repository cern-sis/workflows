class UnknownFileExtension(Exception):
    def __init__(self, file):
        super().__init__(f"Unknown file extension: {file}")
        self.extension = file


class DirectoryNotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NotConnectedException(Exception):
    def __init__(self):
        super().__init__("SFTP connection not established")


class RequiredFieldNotFoundExtractionError(Exception):
    def __init__(self, missing_field):
        super().__init__(f"Required filed is missing: {missing_field}")
        self.missing_field = missing_field


class UnknownLicense(Exception):
    def __init__(self, license):
        super().__init__(f"Unknown license type: {license}")
        self.license = license
