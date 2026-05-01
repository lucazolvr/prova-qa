from __future__ import annotations

from pathlib import Path

from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage


EVIDENCE_DIR = Path("docs/evidencias")


def save_evidence(driver, name: str) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(EVIDENCE_DIR / name))


def test_checkout_e2e(driver, settings):
    login_page = LoginPage(driver, settings.explicit_wait_seconds)
    inventory_page = InventoryPage(driver, settings.explicit_wait_seconds)
    cart_page = CartPage(driver, settings.explicit_wait_seconds)
    checkout_page = CheckoutPage(driver, settings.explicit_wait_seconds)

    save_evidence(driver, "01-login.png")
    login_page.login(settings.login_user, settings.login_password)

    assert inventory_page.get_title() == "Products"
    save_evidence(driver, "02-inventario.png")

    inventory_page.add_backpack_to_cart()
    assert inventory_page.get_cart_count() == "1"
    save_evidence(driver, "03-produto-no-carrinho.png")

    inventory_page.open_cart()
    assert cart_page.has_backpack() is True
    save_evidence(driver, "04-carrinho.png")

    cart_page.start_checkout()
    checkout_page.wait_for_information_step()
    save_evidence(driver, "05-checkout-informacoes.png")

    checkout_page.fill_customer_information(
        first_name="QA",
        last_name="Automation",
        postal_code="89000000",
    )
    checkout_page.wait_for_overview_step()
    save_evidence(driver, "06-checkout-resumo.png")

    checkout_page.finish_checkout()

    assert checkout_page.get_success_message() == "Thank you for your order!"
    save_evidence(driver, "07-compra-finalizada.png")
