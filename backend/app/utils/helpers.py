import logging
logger = logging.getLogger("sentinelqa")

def safe_get(d, key, default=None):
    try:
        return d.get(key, default)
    except Exception:
        return default

def setup_logging():
    import sys
    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
