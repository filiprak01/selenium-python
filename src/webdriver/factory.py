"""Configurable local WebDriver factory."""

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

from webdriver.chrome_options import build_chrome_options

DEFAULT_BROWSER = "chrome"


def create_webdriver(
    browser: str = DEFAULT_BROWSER,
    *,
    headless: bool = False,
    download_directory: Path | str | None = None,
    driver_path: Path | str | None = None,
) -> WebDriver:
    """Create a local WebDriver for the configured browser.

    Chrome is intentionally the only implementation for now. The browser argument
    remains explicit so adding another local browser does not change client APIs.
    """

    browser_name = browser.strip().lower()
    if browser_name != DEFAULT_BROWSER:
        raise ValueError(f"Unsupported browser {browser!r}. Supported browsers: {DEFAULT_BROWSER}.")

    options = build_chrome_options(
        headless=headless,
        download_directory=download_directory,
    )
    if driver_path is None:
        return webdriver.Chrome(options=options)

    service = Service(executable_path=str(Path(driver_path).expanduser()))
    return webdriver.Chrome(service=service, options=options)
