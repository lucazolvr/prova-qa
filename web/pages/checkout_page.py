from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutPage:
    TITLE = (By.CSS_SELECTOR, "span.title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "h2.complete-header")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_information_step(self) -> None:
        self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Checkout: Your Information"))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))

    def fill_customer_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.wait_for_information_step()
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def wait_for_overview_step(self) -> None:
        self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Checkout: Overview"))
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))

    def finish_checkout(self) -> None:
        self.wait_for_overview_step()
        self.driver.find_element(*self.FINISH_BUTTON).click()

    def get_success_message(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
