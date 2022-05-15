import re
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


def collapse_initials(name):
    if len(name.split(".")) > 1:
        name = re.sub(r"([A-Z]\.)[\s\-]+(?=[A-Z]\.)", r"\1", name)
    return name


def split_fullname(author):
    if not author:
        return "", ""

    surname_first = "," in author
    fullname = [n.strip() for n in author.split("," if surname_first else " ")]

    return (
        (fullname[0], " ".join(fullname[1:]))
        if surname_first
        else (fullname[-1], " ".join(fullname[:-1]))
    )


def parse_authors(author):
    if "raw_name" in author and "surname" not in author:
        author["surname"], author["given_names"] = split_fullname(author["raw_name"])
    if "given_names" in author and author["given_names"]:
        author["given_names"] = collapse_initials(author["given_names"])
        author["full_name"] = "{0}, {1}".format(
            author["surname"], author["given_names"]
        )
    else:
        author["full_name"] = author["surname"]

    return author
