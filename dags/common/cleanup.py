import re

from bleach import clean
from bleach.html5lib_shim import Filter
from bleach.sanitizer import Cleaner


def clean_whitespace_characters(input: str):
    return " ".join(input.split())


def convert_html_subsripts_to_latex(input):
    from re import sub

    input = sub("<sub>(.*?)</sub>", r"$_{\1}$", input)
    input = sub("<inf>(.*?)</inf>", r"$_{\1}$", input)
    input = sub("<sup>(.*?)</sup>", r"$^{\1}$", input)
    return input


def clean_collaboration(input):
    return clean_whitespace_characters(input.replace("for the", ""))


def remove_specific_tags(value, tags=None, attributes=None):
    tags = tags or {}
    attributes = attributes or {}
    return clean(value, tags=tags, attributes=attributes, strip=True)


class RemoveLabelTagsContentFilter(Filter):
    def __iter__(self):
        label_tag = False
        for token in super().__iter__():
            if token["type"] == "StartTag" and token["name"] == "label":
                label_tag = True
            elif token["type"] == "EndTag" and token["name"] == "label":
                label_tag = False
            elif label_tag:
                token["data"] = ""
            yield token


def clean_affiliation_for_author(input):
    cleaner = Cleaner(
        filters=[RemoveLabelTagsContentFilter], tags={"label"}, strip=True
    )
    cleaned_label_content = cleaner.clean(input)
    return clean_whitespace_characters(remove_specific_tags(cleaned_label_content))


def clean_all_affiliations_for_author(data):
    for affiliation in data.get("affiliations", []):
        affiliation["value"] = clean_affiliation_for_author(affiliation["value"])
    return data


def remove_unnecessary_fields(obj):
    fieldnames = [
        "curated",
        "citeable",
        "files",
        "date_published",
        "source_file_path",
        "local_files",
    ]
    [obj.pop(field, None) for field in fieldnames]
    return obj


def remove_orcid_prefix(obj):
    pattern = re.compile(r"https{0,1}://orcid.org/|orcid-|orcid:", flags=re.I)
    for author in obj.get("authors", ()):
        if "orcid" not in author:
            continue
        author["orcid"] = pattern.sub("", author["orcid"])
    return obj
