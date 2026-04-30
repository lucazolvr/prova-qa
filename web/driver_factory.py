from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from web.config.settings import Settings


def _build_chrome(settings: Settings) -> webdriver.Chrome:
    options = ChromeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(settings.implicit_wait_seconds)
    return driver


def _build_edge(settings: Settings) -> webdriver.Edge:
    options = EdgeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-gpu")
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(settings.implicit_wait_seconds)
    return driver


def create_driver(settings: Settings):
    if settings.browser == "edge":
        return _build_edge(settings)
    return _build_chrome(settings)
