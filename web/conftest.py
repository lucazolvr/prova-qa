from __future__ import annotations

from pathlib import Path

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from web.config.settings import get_settings
from web.driver_factory import create_driver

DEBUG_DIR = Path("tmp/selenium-debug")


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture()
def driver(settings):
    browser = create_driver(settings)
    browser.get(settings.base_url)
    yield browser
    browser.quit()


@pytest.fixture()
def wait(driver, settings):
    return WebDriverWait(driver, settings.explicit_wait_seconds)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            DEBUG_DIR.mkdir(parents=True, exist_ok=True)
            name = item.name.replace("/", "_")
            try:
                (DEBUG_DIR / f"{name}.url.txt").write_text(
                    driver.current_url, encoding="utf-8"
                )
                (DEBUG_DIR / f"{name}.html").write_text(
                    driver.page_source, encoding="utf-8"
                )
                driver.save_screenshot(str(DEBUG_DIR / f"{name}.png"))
            except Exception:
                pass
