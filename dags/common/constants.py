import re

ARXIV_EXTRACTION_PATTERN = re.compile(r"(arxiv:|v[0-9]$)", flags=re.I)
NODE_ATTRIBUTE_NOT_FOUND_ERRORS = (AttributeError, TypeError)
COUNTRY_PARSING_PATTERN = re.compile(r"\b[A-Z]*[a-z]*$")
ORGANIZATION_PARSING_PATTERN = re.compile(r",\s\b[A-Z]*[a-z]*$")
