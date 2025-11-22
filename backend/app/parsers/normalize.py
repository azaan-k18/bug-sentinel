import re

_ts_pattern = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?Z?")
_unix_path = re.compile(r"/[A-Za-z0-9_\-./]+")
_windows_path = re.compile(r"[A-Za-z]:\\[A-Za-z0-9_\\.\-]+")
_url = re.compile(r"https?://\S+")
_line_no = re.compile(r"\bline\s*\d+\b", flags=re.IGNORECASE)

def normalize_message(msg: str) -> str:
    if not msg:
        return ""
    msg = _ts_pattern.sub(" ", msg)
    msg = _url.sub(" ", msg)
    msg = _windows_path.sub(" ", msg)
    msg = _unix_path.sub(" ", msg)
    msg = _line_no.sub(" ", msg)
    msg = re.sub(r"\s+", " ", msg).strip()
    return msg.lower()
