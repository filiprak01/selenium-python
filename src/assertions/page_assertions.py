"""Wait-backed assertions for common page state."""

import logging
from collections.abc import Callable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait

from models.constants import (
    DEFAULT_ELEMENT_VISIBILITY_TIMEOUT_SECONDS,
    DEFAULT_POLL_INTERVAL_SECONDS,
)

Locator = tuple[str, str]
LOGGER = logging.getLogger(__name__)
DEFAULT_ASSERTION_TIMEOUT_SECONDS: float = float(DEFAULT_ELEMENT_VISIBILITY_TIMEOUT_SECONDS)
DEFAULT_ASSERTION_POLL_FREQUENCY_SECONDS: float = float(DEFAULT_POLL_INTERVAL_SECONDS)


def assert_page_title(
    driver: WebDriver,
    expected_title: str,
    timeout: float = DEFAULT_ASSERTION_TIMEOUT_SECONDS,
) -> None:
    """Assert that the browser title becomes exactly ``expected_title``."""

    try:
        _wait(driver, timeout, expected.title_is(expected_title))
    except TimeoutException as error:
        raise AssertionError(
            f"Expected page title to be {expected_title!r} within {timeout} seconds; "
            f"actual title was {driver.title!r}."
        ) from error


def assert_current_url(
    driver: WebDriver,
    expected_url: str,
    timeout: float = DEFAULT_ASSERTION_TIMEOUT_SECONDS,
) -> None:
    """Assert that the current URL becomes exactly ``expected_url``."""

    try:
        _wait(driver, timeout, expected.url_to_be(expected_url))
    except TimeoutException as error:
        raise AssertionError(
            f"Expected URL to be {expected_url!r} within {timeout} seconds; "
            f"actual URL was {driver.current_url!r}."
        ) from error


def assert_element_visible(
    driver: WebDriver,
    locator: Locator,
    timeout: float = DEFAULT_ASSERTION_TIMEOUT_SECONDS,
    poll_frequency: float | None = DEFAULT_ASSERTION_POLL_FREQUENCY_SECONDS,
) -> None:
    """Assert that the element identified by ``locator`` becomes visible."""

    effective_poll_frequency = (
        DEFAULT_ASSERTION_POLL_FREQUENCY_SECONDS if poll_frequency is None else poll_frequency
    )
    LOGGER.info(
        "Waiting up to %.2f seconds for element %r to become visible "
        "with a %.2f-second poll frequency.",
        timeout,
        locator,
        effective_poll_frequency,
    )
    try:
        _wait(
            driver,
            timeout,
            expected.visibility_of_element_located(locator),
            effective_poll_frequency,
        )
    except TimeoutException as error:
        LOGGER.warning(
            "Timed out after %.2f seconds while waiting for element %r to become visible.",
            timeout,
            locator,
        )
        raise AssertionError(
            f"Element {locator!r} was not visible within {timeout} seconds "
            f"using a {effective_poll_frequency}-second poll frequency."
        ) from error


def assert_element_text(
    driver: WebDriver,
    locator: Locator,
    expected_text: str,
    timeout: float = DEFAULT_ASSERTION_TIMEOUT_SECONDS,
) -> None:
    """Assert that a visible element contains ``expected_text``."""

    def text_is_present(current_driver: WebDriver) -> bool:
        element = current_driver.find_element(*locator)
        return element.is_displayed() and expected_text in element.text

    try:
        _wait(driver, timeout, text_is_present)
    except TimeoutException as error:
        actual_text = driver.find_element(*locator).text
        raise AssertionError(
            f"Expected element {locator!r} to contain {expected_text!r}; "
            f"actual text was {actual_text!r}."
        ) from error


def _wait(
    driver: WebDriver,
    timeout: float,
    condition: Callable[[WebDriver], object],
    poll_frequency: float | None = None,
) -> object:
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")
    if poll_frequency is not None and poll_frequency <= 0:
        raise ValueError("poll_frequency must be greater than zero")
    if poll_frequency is None:
        return WebDriverWait(driver, timeout).until(condition)
    return WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(condition)
