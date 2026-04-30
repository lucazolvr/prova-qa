from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    base_url: str
    login_user: str
    login_password: str
    browser: str
    chrome_binary: str | None
    headless: bool
    implicit_wait_seconds: int
    explicit_wait_seconds: int


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _optional_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def get_settings() -> Settings:
    return Settings(
        base_url=os.getenv("BASE_URL", "https://www.saucedemo.com/"),
        login_user=os.getenv("LOGIN_USER", "standard_user"),
        login_password=os.getenv("LOGIN_PASSWORD", "secret_sauce"),
        browser=os.getenv("BROWSER", "chrome").strip().lower(),
        chrome_binary=_optional_env("CHROME_BINARY"),
        headless=_bool_env("HEADLESS", True),
        implicit_wait_seconds=int(os.getenv("IMPLICIT_WAIT_SECONDS", "0")),
        explicit_wait_seconds=int(os.getenv("EXPLICIT_WAIT_SECONDS", "10")),
    )
