from __future__ import annotations

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from web.config.settings import get_settings
from web.driver_factory import create_driver


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
