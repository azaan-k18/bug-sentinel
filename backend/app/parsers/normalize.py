import re

def normalize_message(msg: str) -> str:
    """
    Strips Jenkins logs, timestamps, file paths, noise.
    Makes text ML-friendly.
    """

    if not msg:
        return ""

    # Remove timestamps like 2024-05-01 12:33:54
    msg = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "", msg)

    # Remove file paths
    msg = re.sub(r"/[A-Za-z0-9_\-./]+", "", msg)

    # Remove line numbers
    msg = re.sub(r"line \d+", "", msg, flags=re.IGNORECASE)

    # Collapse whitespace
    msg = re.sub(r"\s+", " ", msg).strip()

    return msg.lower()
