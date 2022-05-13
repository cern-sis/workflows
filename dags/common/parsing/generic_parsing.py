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
