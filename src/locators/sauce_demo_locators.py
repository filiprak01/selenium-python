"""Stable selectors for the Sauce Demo application."""

from typing import Final

from selenium.webdriver.common.by import By

Locator = tuple[str, str]


class SauceDemoLocators:
    """Selectors for the first Sauce Demo page under test."""

    LOGO: Final[Locator] = (By.CSS_SELECTOR, "img[alt='Sauce Demo']")
