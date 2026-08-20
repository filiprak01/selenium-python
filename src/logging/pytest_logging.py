"""Allure evidence helpers for failed browser tests."""

import json
from contextlib import suppress

import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.remote.webdriver import WebDriver


def attach_browser_evidence(browser: WebDriver) -> None:
    """Attach screenshot, page source, and browser logs to the current Allure result."""

    with suppress(Exception):
        allure.attach(
            browser.get_screenshot_as_png(),
            name="failure-screenshot",
            attachment_type=AttachmentType.PNG,
        )

    with suppress(Exception):
        allure.attach(
            browser.page_source,
            name="failure-page-source",
            attachment_type=AttachmentType.HTML,
        )

    with suppress(Exception):
        browser_logs = browser.get_log("browser")
        allure.attach(
            json.dumps(browser_logs, indent=2),
            name="failure-browser-logs",
            attachment_type=AttachmentType.JSON,
        )
