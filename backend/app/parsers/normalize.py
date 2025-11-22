import re

def normalize_error_message(raw_text: str) -> str:
    """
    Reduce noise from a raw failure block:
    - Keep the top-most meaningful line
    - Remove file paths and long stack traces
    - Return a short summary (<= 300 chars)
    """
    if not raw_text:
        return ""
    # remove long stack traces
    # take first 10 lines as candidate
    lines = [l.strip() for l in raw_text.strip().splitlines() if l.strip()]
    candidate = ""
    # try to find a line with "Exception" or "AssertionError" etc
    for line in lines[:10]:
        if any(keyword in line for keyword in ["Exception", "Error", "Assertion", "Traceback", "FAILED", "NoSuchElement"]):
            candidate = line
            break
    if not candidate and lines:
        candidate = lines[0]
    # remove file paths, long hex addresses
    candidate = re.sub(r"(/[\w\-\./]+)+", "<PATH>", candidate)
    candidate = re.sub(r"0x[0-9a-fA-F]+", "<ADDR>", candidate)
    candidate = re.sub(r"\s+", " ", candidate)
    return candidate[:300]
