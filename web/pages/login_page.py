from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_BANNER = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))

    def login(self, username: str, password: str) -> None:
        self.wait_until_loaded()
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        self.wait.until(EC.url_contains("inventory.html"))

    def get_error_message(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_BANNER)).text
