from datetime import date, timedelta


class APSParams:
    def __init__(
        self,
        from_date: str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
        until_date: str = date.today().strftime("%Y-%m-%d"),
        date: str = "published",
        journals: str = "",
        sets: str = "",
        per_page: int = 100,
    ):
        self.from_date = from_date
        self.until_date = until_date
        self.date = date
        self.journals = journals
        self.sets = sets
        self.per_page = per_page

    def get_params(self) -> dict:
        params = {
            "from": self.from_date,
            "until": self.until_date,
            "date": self.date,
            "journals": self.journals,
            "sets": self.sets,
            "per_page": self.per_page,
        }
        return {key: value for key, value in params.items() if value}
