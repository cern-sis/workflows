import datetime
import json
import re

from common.exceptions import UnknownFileExtension
from structlog import get_logger

logger = get_logger()


def set_harvesting_interval(repo, **kwargs):
    if (
        "params" in kwargs
        and kwargs["params"].get("start_date")
        and kwargs["params"].get("until_date")
    ):
        return {
            "start_date": kwargs["params"]["start_date"],
            "until_date": kwargs["params"]["until_date"],
        }
    start_date = (
        kwargs.get("params", {}).get("start_date")
        or repo.find_the_last_uploaded_file_date()
    )
    until_date = datetime.date.today().strftime("%Y-%m-%d")
    return {
        "start_date": (start_date or until_date),
        "until_date": until_date,
    }


def construct_license(url, license_type, version):
    if url and license_type and version:
        return {"url": url, "license": f"CC-{license_type}-{version}"}
    logger.error(
        "License is not given, or missing arguments.",
    )


def is_json_serializable(x):
    try:
        json.dumps(x)
        return True
    except TypeError:
        return False


def check_value(value):
    json_serializable = is_json_serializable(value)
    if json_serializable:
        if value:
            return bool(value)
        if "hasattr" in dir(value) and value.hasattr("__iter__"):
            return all(value)
        return False
    return False


def parse_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.error("Cannot parse to integer", value=value)


def extract_text(article, path, field_name, dois):
    try:
        return article.find(path).text
    except AttributeError:
        logger.error(f"{field_name} is not found in XML", dois=dois)
        return


def append_file_if_not_in_excluded_directory(
    filename, exclude_directories, list_of_files
):
    if not exclude_directories or not (
        any(re.search(exclude, filename) for exclude in exclude_directories)
    ):
        list_of_files.append(filename)


def find_extension(file):
    if file.endswith(".xml"):
        return "xml"
    elif file.endswith(".pdf"):
        return "pdf"
    raise UnknownFileExtension(file)
