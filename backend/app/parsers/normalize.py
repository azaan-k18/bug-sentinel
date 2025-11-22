import re

# Existing patterns
_ts_pattern = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?Z?")
_unix_path = re.compile(r"/[A-Za-z0-9_\-./]+")
_windows_path = re.compile(r"[A-Za-z]:\\[A-Za-z0-9_\\.\-]+")
_url = re.compile(r"https?://\S+")
_line_no = re.compile(r"\bline\s*\d+\b", flags=re.IGNORECASE)

# --- NEW PATTERNS ---
_selector = re.compile(r"(#|\.|css=|xpath=|//)[A-Za-z0-9_\-\.\/\[\]\(\)=]+")
_hex = re.compile(r"0x[0-9a-f]+")
_number = re.compile(r"\b\d+\b")
_stack_trace = re.compile(r"^\s*at\s+.*$", flags=re.MULTILINE)
_ip = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")

def normalize_message(msg: str) -> str:
    """Normalize raw logs into stable patterns for ML and grouping."""
    if not msg:
        return ""

    # lowercase
    msg = msg.lower()

    # timestamps
    msg = _ts_pattern.sub(" <timestamp> ", msg)

    # URLs
    msg = _url.sub(" <url> ", msg)

    # file paths
    msg = _windows_path.sub(" <path> ", msg)
    msg = _unix_path.sub(" <path> ", msg)

    # IP addresses
    msg = _ip.sub(" <ip> ", msg)

    # CSS/xpath selectors
    msg = _selector.sub(" <selector> ", msg)

    # hex numbers (memory addresses, ids)
    msg = _hex.sub(" <hex> ", msg)

    # remove stack trace lines completely
    msg = _stack_trace.sub(" ", msg)

    # replace numbers (timeouts, ports, durations)
    msg = _number.sub(" <num> ", msg)

    # line numbers
    msg = _line_no.sub(" <line> ", msg)

    # cleanup spaces
    msg = re.sub(r"\s+", " ", msg).strip()

    return msg