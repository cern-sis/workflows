from datetime import date, timedelta


class HindawiParams:
    def __init__(
        self,
        from_date= (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
        until_date= date.today().strftime("%Y-%m-%d"),
        verb= "listrecords",
        set= "HINDAWI.AHEP",
        metadataprefix= "marc21",
        record= "",
    ):
        self.from_date = from_date
        self.until_date = until_date
        self.verb = verb
        self.set = set
        self.metadataprefix = metadataprefix
        self.record = record

    def _single_record_payload(self, identifier):
        params = {
            "verb": "getrecord",
            "set": self.set,
            "identifier": identifier,
            "metadataprefix": self.metadataprefix,
        }
        return params

    def _set_of_records(self):
        params = {
            "from": self.from_date,
            "until": self.until_date,
            "verb": self.verb,
            "set": self.set,
            "metadataprefix": self.metadataprefix,
        }
        return params

    def get_params(self):
        if self.record:
            identifier = f"oai:hindawi.com:{self.record}"
            params = self._single_record_payload(identifier)
        else:
            params = self._set_of_records()
        return {key: value for key, value in params.items() if value}
