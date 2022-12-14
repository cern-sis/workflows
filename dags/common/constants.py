import re

ARXIV_EXTRACTION_PATTERN = re.compile(r"(arxiv:|v[0-9]$)", flags=re.I)
