"""WebDriver construction and browser options."""

from webdriver.chrome_options import build_chrome_options
from webdriver.factory import create_webdriver

__all__ = ["build_chrome_options", "create_webdriver"]
