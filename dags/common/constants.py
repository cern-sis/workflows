import re

ARXIV_EXTRACTION_PATTERN = re.compile(r"(arxiv:|v[0-9]$)", flags=re.I)
NODE_ATTRIBUTE_NOT_FOUND_ERRORS = (AttributeError, TypeError)
