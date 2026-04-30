from __future__ import annotations

from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.pages.inventory_page import InventoryPage
from web.pages.login_page import LoginPage


def test_checkout_e2e(driver, settings):
    login_page = LoginPage(driver, settings.explicit_wait_seconds)
    inventory_page = InventoryPage(driver, settings.explicit_wait_seconds)
    cart_page = CartPage(driver, settings.explicit_wait_seconds)
    checkout_page = CheckoutPage(driver, settings.explicit_wait_seconds)

    login_page.login(settings.login_user, settings.login_password)

    assert inventory_page.get_title() == "Products"

    inventory_page.add_backpack_to_cart()
    assert inventory_page.get_cart_count() == "1"

    inventory_page.open_cart()
    assert cart_page.has_backpack() is True

    cart_page.start_checkout()
    checkout_page.fill_customer_information(
        first_name="QA",
        last_name="Automation",
        postal_code="89000000",
    )
    checkout_page.finish_checkout()

    assert checkout_page.get_success_message() == "Thank you for your order!"
