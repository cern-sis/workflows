from datetime import date


def take_first(arr):
    try:
        return next(filter(None, arr))
    except StopIteration:
        return None


def list_to_value_dict(arr, key="value"):
    return [{key: val} for val in arr if val]


def join(arr, separator=" "):
    return separator.join(filter(None, arr))


def classification_numbers(arr, standard="PACS"):
    return [{"standard": standard, "classification_number": val} for val in arr if val]


def free_keywords(arr, source="author"):
    return [{"source": source, "value": val} for val in arr if val]


def fix_publication_date(pub_date):
    if not pub_date:
        return ""

    def inner_fix(splitted):
        return splitted if len(splitted) == 3 else inner_fix(splitted + ["1"])

    year, month, day = map(int, inner_fix(pub_date.split("-")))
    tmp_date = date(year, month, day)
    return f"{tmp_date.year:04d}-{tmp_date.month:02d}-{tmp_date.day:02d}"
