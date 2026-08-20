"""Page object for the Sauce Demo home page."""

from assertions.page_assertions import assert_element_visible
from locators.sauce_demo_locators import SauceDemoLocators
from pages.base_page import BasePage


class SauceDemoHomePage(BasePage):
    """Represent the Sauce Demo home page and its loaded-state assertion."""

    def assert_loaded(
        self,
        timeout: float | None = None,
        poll_frequency: float | None = None,
    ) -> None:
        """Assert that the Sauce Demo logo is visible."""

        assert_element_visible(
            self.driver,
            SauceDemoLocators.LOGO,
            timeout=self.timeout if timeout is None else timeout,
            poll_frequency=(self.poll_frequency if poll_frequency is None else poll_frequency),
        )
