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


def parse_author(author):
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


def parse_thesis_supervisors(value):
    value = parse_author(value)
    return {
        "full_name": value.get("full_name"),
        "affiliations": value.get("affiliations"),
    }


def publication_info(article):
    if "publication_info" in article:
        return article["publication_info"]
    return [
        {
            "journal_title": article.get("journal_title", ""),
            "journal_volume": article.get("journal_volume", ""),
            "year": int(article.get("journal_year", 0)) or "",
            "journal_issue": article.get("journal_issue", ""),
            "artid": article.get("journal_artid", ""),
            "page_start": article.get("journal_fpage", ""),
            "page_end": article.get("journal_lpage", ""),
            "material": article.get("journal_doctype", ""),
            "pubinfo_freetext": article.get("pubinfo_freetext", ""),
        }
    ]


def merge_dois(article):
    return article["dois"] + article.get("related_article_doi", [])


def clear_unnecessary_fields(article):
    new_article = article.copy()
    field_list = [
        "journal_title",
        "journal_volume",
        "journal_year",
        "journal_issue",
        "journal_artid",
        "journal_fpage",
        "journal_lpage",
        "journal_doctype",
        "pubinfo_freetext",
        "related_article_doi",
    ]
    [new_article.pop(field_name, "") for field_name in field_list]
    return new_article


def remove_empty_values(obj):
    if isinstance(obj, dict):
        return {
            key: new_val
            for (key, val) in obj.items()
            if (new_val := remove_empty_values(val)) is not None
        } or None
    elif isinstance(obj, (list, tuple, set)):
        return [
            new_val for val in obj if (new_val := remove_empty_values(val)) is not None
        ] or None
    elif obj or obj is False or obj == 0:
        return obj
    return None
