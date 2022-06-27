from datetime import date


def set_harvesting_interval(repo, **kwargs):
    if (
        "params" in kwargs
        and "start_date" in kwargs["params"]
        and "until_date" in kwargs["params"]
    ):
        return {
            "start_date": kwargs["params"]["start_date"],
            "until_date": kwargs["params"]["until_date"],
        }
    start_date = repo.find_the_last_uploaded_file_date()
    until_date = date.today()

    return {
        "start_date": (start_date or until_date).strftime("%Y-%m-%d"),
        "until_date": until_date.strftime("%Y-%m-%d"),
    }
