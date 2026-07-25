import logging
import sys


def configure_logging():
    # Simple logging config; replace with structlog / JSON in prod as needed.
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler.setFormatter(formatter)
    root.handlers = [handler]
    root.setLevel(logging.INFO)
