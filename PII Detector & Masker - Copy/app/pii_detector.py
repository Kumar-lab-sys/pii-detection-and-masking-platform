import re

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
PHONE_REGEX = r"\b\d{10}\b"

def detect_pii(value):
    results = []
    if not isinstance(value, str):
        return results
    if re.fullmatch(EMAIL_REGEX, value):
        results.append("EMAIL")
    if re.fullmatch(PHONE_REGEX, value):
        results.append("PHONE")
    return results
