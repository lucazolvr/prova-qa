from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    TITLE = (By.CSS_SELECTOR, "span.title")
    CART_BADGE = (By.CSS_SELECTOR, "span.shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, "a.shopping_cart_link")
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Products"))
        self.wait.until(EC.element_to_be_clickable(self.BACKPACK_ADD_BUTTON))

    def add_backpack_to_cart(self) -> None:
        self.wait_until_loaded()
        btn = self.wait.until(EC.element_to_be_clickable(self.BACKPACK_ADD_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.text_to_be_present_in_element(self.CART_BADGE, "1"))

    def open_cart(self) -> None:
        cart_link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))
        self.driver.execute_script("arguments[0].click();", cart_link)
        self.wait.until(EC.url_contains("cart.html"))

    def get_title(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def get_cart_count(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.CART_BADGE)).text
