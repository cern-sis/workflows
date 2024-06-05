import re

from six import string_types

SPLIT_KEY_PATTERN = re.compile(r"\.|\[")


def get_value(record, key, default=None):
    """Return item as `dict.__getitem__` but using 'smart queries'.

    .. note::

        Accessing one value in a normal way, meaning d['a'], is almost as
        fast as accessing a regular dictionary. But using the special
        name convention is a bit slower than using the regular access:
        .. code-block:: python
            >>> %timeit x = dd['a[0].b']
            100000 loops, best of 3: 3.94 us per loop
            >>> %timeit x = dd['a'][0]['b']
            1000000 loops, best of 3: 598 ns per loop
    """

    def getitem(k, v, default):
        if isinstance(v, string_types):
            raise KeyError
        elif isinstance(v, dict):
            return v[k]
        elif "]" in k:
            k = k[:-1].replace("n", "-1")
            # Work around for list indexes and slices
            try:
                return v[int(k)]
            except IndexError:
                return default
            except ValueError:
                return v[
                    slice(
                        *map(
                            lambda x: int(x.strip()) if x.strip() else None,
                            k.split(":"),
                        )
                    )
                ]
        else:
            tmp = []
            for inner_v in v:
                try:
                    tmp.append(getitem(k, inner_v, default))
                except KeyError:
                    continue
            return tmp

    # Wrap a top-level list in a dict
    if isinstance(record, list):
        record = {"record": record}
        key = ".".join(["record", key])

    # Check if we are using python regular keys
    try:
        return record[key]
    except KeyError:
        pass

    keys = SPLIT_KEY_PATTERN.split(key)
    value = record
    for k in keys:
        try:
            value = getitem(k, value, default)
        except KeyError:
            return default
    return value
