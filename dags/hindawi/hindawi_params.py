from datetime import date, timedelta


class HindawiParams:
    def __init__(
        self,
        from_date: str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
        until_date: str = date.today().strftime("%Y-%m-%d"),
        verb: str = "listrecords",
        set: str = "HINDAWI.AHEP",
        metadataprefix: str = "marc21",
    ):
        self.from_date = from_date
        self.until_date = until_date
        self.verb = verb
        self.set = set
        self.metadataprefix = metadataprefix

    def get_params(self) -> dict:
        params = {
            "from": self.from_date,
            "until": self.until_date,
            "verb": self.verb,
            "set": self.set,
            "metadataprefix": self.metadataprefix,
        }
        return {key: value for key, value in params.items() if value}
