"""Common explicit-wait behavior for Selenium page objects."""

import logging
from collections.abc import Callable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]
LOGGER = logging.getLogger(__name__)
DEFAULT_PAGE_TIMEOUT_SECONDS: float = 10.0


class BasePage:
    """Base class hiding low-level Selenium synchronization from tests."""

    def __init__(
        self,
        driver: WebDriver,
        timeout: float = DEFAULT_PAGE_TIMEOUT_SECONDS,
        poll_frequency: float | None = None,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if poll_frequency is not None and poll_frequency <= 0:
            raise ValueError("poll_frequency must be greater than zero")
        self._driver = driver
        self._timeout = timeout
        self._poll_frequency = poll_frequency

    @property
    def driver(self) -> WebDriver:
        """Return the page's WebDriver for framework extensions."""

        return self._driver

    @property
    def timeout(self) -> float:
        """Return the default explicit wait timeout."""

        return self._timeout

    @property
    def poll_frequency(self) -> float | None:
        """Return the configured wait poll frequency, if one was provided."""

        return self._poll_frequency

    def find(self, locator: Locator) -> WebElement:
        """Return a visible element identified by ``locator``."""

        return self.wait_for_visible(locator)

    def wait_for_presence(
        self,
        locator: Locator,
        poll_frequency: float | None = None,
    ) -> WebElement:
        """Wait until an element is present in the DOM."""

        return self._wait(
            expected.presence_of_element_located(locator),
            poll_frequency=poll_frequency,
        )

    def wait_for_visible(
        self,
        locator: Locator,
        poll_frequency: float | None = None,
    ) -> WebElement:
        """Wait until an element is present and visible."""

        return self._wait(
            expected.visibility_of_element_located(locator),
            poll_frequency=poll_frequency,
        )

    def wait_for_clickable(
        self,
        locator: Locator,
        poll_frequency: float | None = None,
    ) -> WebElement:
        """Wait until an element can be clicked."""

        return self._wait(
            expected.element_to_be_clickable(locator),
            poll_frequency=poll_frequency,
        )

    def click(self, locator: Locator) -> None:
        """Click a user-visible element after it becomes actionable."""

        self.wait_for_clickable(locator).click()

    def fill(self, locator: Locator, value: str, clear: bool = True) -> None:
        """Enter text into an input after it becomes visible."""

        element = self.wait_for_visible(locator)
        if clear:
            element.clear()
        element.send_keys(value)

    def read_text(self, locator: Locator) -> str:
        """Read the text of a visible element."""

        return self.wait_for_visible(locator).text

    def is_visible(
        self,
        locator: Locator,
        timeout: float | None = None,
        poll_frequency: float | None = None,
    ) -> bool:
        """Return whether an element becomes visible before the timeout."""

        wait_timeout = self._timeout if timeout is None else timeout
        if wait_timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        effective_poll_frequency = self._get_poll_frequency(poll_frequency)
        LOGGER.info(
            "Waiting up to %.2f seconds for element %r to become visible "
            "with a %s-second poll frequency.",
            wait_timeout,
            locator,
            "WebDriver default"
            if effective_poll_frequency is None
            else f"{effective_poll_frequency:.2f}",
        )
        try:
            self._create_wait(wait_timeout, effective_poll_frequency).until(
                expected.visibility_of_element_located(locator)
            )
        except TimeoutException:
            LOGGER.warning(
                "Timed out after %.2f seconds while waiting for element %r to become visible.",
                wait_timeout,
                locator,
            )
            return False
        return True

    def open(self, url: str) -> None:
        """Navigate the page object to an absolute URL."""

        self._driver.get(url)

    def _wait(
        self,
        condition: Callable[[WebDriver], WebElement | bool],
        poll_frequency: float | None = None,
    ) -> WebElement:
        effective_poll_frequency = self._get_poll_frequency(poll_frequency)
        LOGGER.info(
            "Waiting up to %.2f seconds for a page condition with a %s-second poll frequency.",
            self._timeout,
            "WebDriver default"
            if effective_poll_frequency is None
            else f"{effective_poll_frequency:.2f}",
        )
        try:
            return self._create_wait(self._timeout, effective_poll_frequency).until(condition)
        except TimeoutException:
            LOGGER.warning("Page condition timed out after %.2f seconds.", self._timeout)
            raise

    def _get_poll_frequency(self, poll_frequency: float | None) -> float | None:
        effective_poll_frequency = (
            self._poll_frequency if poll_frequency is None else poll_frequency
        )
        if effective_poll_frequency is not None and effective_poll_frequency <= 0:
            raise ValueError("poll_frequency must be greater than zero")
        return effective_poll_frequency

    def _create_wait(
        self,
        timeout: float,
        poll_frequency: float | None,
    ) -> WebDriverWait[WebDriver]:
        if poll_frequency is None:
            return WebDriverWait(self._driver, timeout)
        return WebDriverWait(self._driver, timeout, poll_frequency=poll_frequency)
