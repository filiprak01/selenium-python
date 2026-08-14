"""Smoke coverage for the first Sauce Demo application page."""

import allure
import pytest

from clients.ui_client import UIClient
from models.configuration import FrameworkConfig
from pages.sauce_demo_home_page import SauceDemoHomePage


@pytest.mark.smoke
@pytest.mark.ui
@allure.feature("Sauce Demo")
@allure.story("Home page loading")
def test_sauce_demo_home_page_loads(
    ui_client: UIClient,
    config: FrameworkConfig,
) -> None:
    """Verify that the Sauce Demo home page loads its logo visibly."""

    with ui_client.step("Open the Sauce Demo home page"):
        ui_client.open(config.environment.base_url)

    home_page = ui_client.page(SauceDemoHomePage)
    with ui_client.step("Verify that the Sauce Demo logo is visible"):
        home_page.assert_loaded(
            timeout=config.timeouts.element_visibility_seconds,
            poll_frequency=config.timeouts.poll_interval_seconds,
        )

    ui_client.capture_screenshot_step("Capture the Sauce Demo home page after loaded assertion")
