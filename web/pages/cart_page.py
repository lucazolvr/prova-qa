from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    TITLE = (By.CSS_SELECTOR, "span.title")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    BACKPACK_ITEM = (By.ID, "item_4_title_link")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Your Cart"))
        self.wait.until(EC.visibility_of_element_located(self.BACKPACK_ITEM))

    def start_checkout(self) -> None:
        self.wait_until_loaded()
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()

    def has_backpack(self) -> bool:
        self.wait_until_loaded()
        return self.driver.find_element(*self.BACKPACK_ITEM).is_displayed()
