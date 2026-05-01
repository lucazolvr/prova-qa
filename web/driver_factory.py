from __future__ import annotations

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from web.config.settings import Settings


def _build_chrome(settings: Settings) -> webdriver.Chrome:
    options = ChromeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-search-engine-choice-screen")
    if settings.chrome_binary:
        options.binary_location = settings.chrome_binary
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(settings.implicit_wait_seconds)
    return driver


def _build_edge(settings: Settings) -> webdriver.Edge:
    options = EdgeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-gpu")
    if settings.chrome_binary:
        options.binary_location = settings.chrome_binary
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(settings.implicit_wait_seconds)
    return driver


def create_driver(settings: Settings):
    browser = settings.browser
    if browser == "edge":
        return _build_edge(settings)
    if browser != "chrome" and os.getenv("CI"):
        return _build_chrome(settings)
    return _build_chrome(settings)
