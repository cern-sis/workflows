import re

ARXIV_EXTRACTION_PATTERN = re.compile(r"(arxiv:|v[0-9]$)", flags=re.I)
NODE_ATTRIBUTE_NOT_FOUND_ERRORS = (AttributeError, TypeError)
COUNTRY_PARSING_PATTERN = re.compile(r"\b[A-Z]*[a-z]*$")
ORGANIZATION_PARSING_PATTERN = re.compile(r",\s\b[A-Z]*[a-z]*$")
REMOVE_SPECIAL_CHARS = re.compile(r"[^A-Za-z0-9\s\,\.]+")
LICENSE_PATTERN = re.compile(r"([A-Za-z]+)\/([0-9]+\.[0-9]+)")
LICENSE_VERSION_PATTERN = re.compile(r"\d{1,}\.\d{1}")
CREATIVE_COMMONS_PATTERN = re.compile(r".*(creative\s{0,}commons).*", flags=re.I)
BY_PATTERN = re.compile(r".*(attribution).*", flags=re.I)
WHITE_SPACES = re.compile(r"[\n\t]{1,}" + r"\s{2,}")
CDATA_PATTERN = re.compile(r"<\?CDATA(.*)\?>")
FN_REGEX = re.compile(r"<fn.*<\/fn>")

JOURNAL_MAPPING = {"PLB": "Physics Letters B", "NUPHB": "Nuclear Physics B"}
