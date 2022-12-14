import re

ARXIV_EXTRACTION_PATTERN = re.compile(r"(arxiv:|v[0-9]$)", flags=re.I)
ARXIV_VALIDATION_PATTERN = re.compile(r"^[0-9]{4}\.[0-9]{5}$")
