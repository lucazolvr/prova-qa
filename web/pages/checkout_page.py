from __future__ import annotations

import json
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutPage:
    TITLE = (By.CSS_SELECTOR, "span.title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_BANNER = (By.CSS_SELECTOR, "h3[data-test='error']")
    FINISH_BUTTON = (By.ID, "finish")
    CHECKOUT_SUMMARY_CONTAINER = (By.ID, "checkout_summary_container")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "h2.complete-header")
    COMPLETE_CONTAINER = (By.ID, "checkout_complete_container")

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _field_state_snapshot(self) -> dict:
        script = """
        const ids = ['first-name', 'last-name', 'postal-code'];
        const fields = Object.fromEntries(ids.map(id => {
          const el = document.getElementById(id);
          return [id, el ? {
            value: el.value,
            placeholder: el.placeholder,
            disabled: el.disabled,
            readOnly: el.readOnly,
            active: document.activeElement === el,
            selectionStart: el.selectionStart,
            selectionEnd: el.selectionEnd,
            className: el.className,
            outerHTML: el.outerHTML
          } : null];
        }));
        return {
          activeElementId: document.activeElement ? document.activeElement.id : null,
          fields
        };
        """
        return self.driver.execute_script(script)

    def _capture_debug_artifacts(self, label: str) -> str:
        artifacts_dir = Path("tmp/selenium-debug")
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = artifacts_dir / f"{label}.png"
        html_path = artifacts_dir / f"{label}.html"
        json_path = artifacts_dir / f"{label}.json"
        self.driver.save_screenshot(str(screenshot_path))
        html_path.write_text(self.driver.page_source, encoding="utf-8")
        json_path.write_text(json.dumps(self._field_state_snapshot(), ensure_ascii=False, indent=2), encoding="utf-8")
        return f"screenshot={screenshot_path.as_posix()} html={html_path.as_posix()} json={json_path.as_posix()}"

    @staticmethod
    def _debug_context(driver: WebDriver) -> str:
        source = driver.page_source[:800].replace("\n", " ")
        return f"url={driver.current_url} title={driver.title!r} source={source}"

    def wait_for_information_step(self) -> None:
        self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Checkout: Your Information"))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))

    def _set_input_value(self, locator: tuple[str, str], value: str) -> str:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            """
            const el = arguments[0];
            const value = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            el.focus();
            setter.call(el, value);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.blur();
            return el.value;
            """,
            element,
            value,
        )
        return self.driver.find_element(*locator).get_attribute("value")

    def fill_customer_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.wait_for_information_step()
        first_value = self._set_input_value(self.FIRST_NAME_INPUT, first_name)
        last_value = self._set_input_value(self.LAST_NAME_INPUT, last_name)
        postal_value = self._set_input_value(self.POSTAL_CODE_INPUT, postal_code)

        if first_value != first_name or last_value != last_name or postal_value != postal_code:
            raise AssertionError(
                "Checkout não reteve os campos esperados. "
                f"first={first_value!r} last={last_value!r} postal={postal_value!r}. "
                f"{self._debug_context(self.driver)} {self._capture_debug_artifacts('checkout-field-retention')}"
            )

        continue_button = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
        continue_button.click()

        if "checkout-step-two.html" not in self.driver.current_url:
            error_banners = self.driver.find_elements(*self.ERROR_BANNER)
            if error_banners and error_banners[0].is_displayed():
                raise AssertionError(
                    f"Checkout exibiu erro de validação: {error_banners[0].text}. {self._debug_context(self.driver)} {self._capture_debug_artifacts('checkout-validation-error')}"
                )

    def wait_for_overview_step(self) -> None:
        try:
            self.wait.until(EC.url_contains("checkout-step-two.html"))
            self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Checkout: Overview"))
            self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_SUMMARY_CONTAINER))
            self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        except TimeoutException as exc:
            raise AssertionError(
                f"Checkout não avançou para overview. {self._debug_context(self.driver)} {self._capture_debug_artifacts('checkout-overview-timeout')}"
            ) from exc

    def finish_checkout(self) -> None:
        self.wait_for_overview_step()
        finish_button = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", finish_button)
        finish_button.click()

    def get_success_message(self) -> str:
        try:
            self.wait.until(EC.url_contains("checkout-complete.html"))
            self.wait.until(EC.text_to_be_present_in_element(self.TITLE, "Checkout: Complete!"))
            self.wait.until(EC.visibility_of_element_located(self.COMPLETE_CONTAINER))
            return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
        except TimeoutException as exc:
            raise AssertionError(
                f"Checkout não chegou à tela final. {self._debug_context(self.driver)} {self._capture_debug_artifacts('checkout-complete-timeout')}"
            ) from exc
