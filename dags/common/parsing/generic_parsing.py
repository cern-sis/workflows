def take_first(arr):
    try:
        return next(filter(None, arr))
    except StopIteration:
        return None
