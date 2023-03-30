import datetime
import json
import re
import xml.etree.ElementTree as ET
from io import StringIO
from stat import S_ISDIR, S_ISREG

from common.constants import (
    BY_PATTERN,
    CDATA_PATTERN,
    CREATIVE_COMMONS_PATTERN,
    LICENSE_PATTERN,
)
from common.exceptions import UnknownFileExtension, UnknownLicense
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


def walk_sftp(sftp, remotedir, paths):
    for entry in sftp.listdir_attr(remotedir):
        remotepath = remotedir + "/" + entry.filename
        mode = entry.st_mode
        if S_ISDIR(mode):
            walk_sftp(sftp=sftp, remotedir=remotepath, paths=paths)
        elif S_ISREG(mode):
            paths.append(remotepath)


def construct_license(license_type, version, url=None):
    if not license_type == "CC-BY":
        raise UnknownLicense(license_type)
    if url and license_type and version:
        return {"url": url, "license": f"{license_type}-{version}"}
    if license_type and version:
        logger.error("License URL is not found in XML.")
        return {"license": f"{license_type}-{version}"}
    logger.error(
        "License is not given, or missing arguments.",
    )


def get_license_type(license_text):
    if not CREATIVE_COMMONS_PATTERN.search(license_text) or not BY_PATTERN.match(
        license_text
    ):
        raise UnknownLicense(license=license_text)
    return "CC-BY"


def get_license_type_and_version_from_url(url):
    match = LICENSE_PATTERN.search(url)
    if not match:
        logger.error("No license found in URL")
        return None
    first_part_of_license_type = ""
    version = match.group(2)
    second_part_of_license_type = match.group(1).upper()
    if CREATIVE_COMMONS_PATTERN.search(url):
        first_part_of_license_type = "CC"
    else:
        raise UnknownLicense(url)
    if not f"{first_part_of_license_type}-{second_part_of_license_type}" == "CC-BY":
        raise UnknownLicense(url)
    license_type = ("-").join([first_part_of_license_type, second_part_of_license_type])
    return construct_license(license_type=license_type, version=version, url=url)


def preserve_cdata(article: str):
    matches = CDATA_PATTERN.finditer(article)
    for match in matches:
        cdata_content_with_escaped_escape_chars = match.group(1).replace("\\", "\\\\")
        article = CDATA_PATTERN.sub(
            cdata_content_with_escaped_escape_chars, article, count=1
        )
    return article


def parse_to_ET_element(article: str):
    return ET.fromstring(preserve_cdata(article))


def parse_without_names_spaces(xml: str):
    it = ET.iterparse(StringIO(xml))
    for _, el in it:
        el.tag = el.tag.rpartition("}")[-1]
    root = it.root
    return root


def get_text_value(element: ET.Element):
    if element is not None:
        if element.text:
            return clean_text(element.text)


def clean_text(text):
    return " ".join(text.split())
