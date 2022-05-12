def take_first(arr):
    try:
        return next(filter(None, arr))
    except StopIteration:
        return None


def list_to_value_dict(arr, key="value"):
    return [{key: val} for val in arr if val]


def join(arr, separator=" "):
    return separator.join(filter(None, arr))
