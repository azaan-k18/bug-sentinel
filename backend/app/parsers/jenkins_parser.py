import re
from typing import List, Dict
from .normalize import normalize_error_message

FAIL_MARKERS = [
    r"^FAILED:.*$",
    r"AssertionError:",
    r"Traceback \(most recent call last\):",
    r"Exception in thread",
    r"ERROR: test",
    r"^FAIL$",
    r"NoSuchElementException",
    r"TimeoutException",
]

MARKER_RE = re.compile("|".join([m for m in FAIL_MARKERS]), re.IGNORECASE | re.MULTILINE)

def extract_failures_from_console(console_text: str) -> List[Dict]:
    """
    Extract likely failure blocks from Jenkins console output.
    Returns list of dicts: {raw: <full block>, summary: <normalized summary>}
    """
    if not console_text:
        return []
    # Heuristic: split into sections using two or more newlines, then filter blocks containing markers
    blocks = re.split(r"\n\s*\n", console_text)
    failures = []
    for b in blocks:
        if MARKER_RE.search(b):
            summary = normalize_error_message(b)
            failures.append({"raw": b.strip(), "summary": summary})
    # if no blocks found, try scanning for single-line exceptions
    if not failures:
        lines = console_text.splitlines()
        for ln in lines[-200:]:  # check last 200 lines
            if MARKER_RE.search(ln):
                failures.append({"raw": ln, "summary": normalize_error_message(ln)})
    return failures