from typing import Generator
from app.core.config import settings


def get_settings() -> Generator:
    yield settings
