"""High-level ownership and page access for a UI test session."""

import logging
import re
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import TypeVar

import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from webdriver.factory import create_webdriver

PageType = TypeVar("PageType", bound=BasePage)
LOGGER = logging.getLogger(__name__)


class UIClient:
    """Own one WebDriver session and provide typed access to page objects."""

    def __init__(
        self,
        driver: WebDriver | None = None,
        *,
        browser: str = "chrome",
        headless: bool = False,
        download_directory: Path | str | None = None,
        screenshot_directory: Path | str | None = None,
        driver_path: Path | str | None = None,
        base_url: str | None = None,
        timeout: float = 10.0,
        screenshots_enabled: bool = True,
        screenshot_after_steps: bool = True,
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        if driver is None:
            driver = create_webdriver(
                browser,
                headless=headless,
                download_directory=download_directory,
                driver_path=driver_path,
            )
        self._driver = driver
        self._base_url = base_url.rstrip("/") if base_url else None
        self._timeout = timeout
        self._screenshot_directory = (
            Path(screenshot_directory) if screenshot_directory is not None else None
        )
        self._screenshots_enabled = screenshots_enabled
        self._screenshot_after_steps = screenshot_after_steps
        self._screenshot_sequence = 0

    @property
    def driver(self) -> WebDriver:
        """Return the session driver for framework-level integrations."""

        return self._driver

    @property
    def base_url(self) -> str | None:
        """Return the optional base URL used by :meth:`open`."""

        return self._base_url

    @property
    def timeout(self) -> float:
        """Return the default timeout passed to created page objects."""

        return self._timeout

    @property
    def screenshot_directory(self) -> Path | None:
        """Return the optional directory used to persist step screenshots."""

        return self._screenshot_directory

    @property
    def screenshots_enabled(self) -> bool:
        """Return whether screenshot evidence is enabled for this client."""

        return self._screenshots_enabled

    @property
    def screenshot_after_steps(self) -> bool:
        """Return whether named UI steps automatically capture screenshots."""

        return self._screenshot_after_steps

    @contextmanager
    def step(self, name: str) -> Iterator[None]:
        """Run an Allure step with lifecycle logging and optional screenshot evidence."""

        step_name = name.strip()
        if not step_name:
            raise ValueError("step name must not be empty")

        LOGGER.info("STEP START | %s", step_name)
        with allure.step(step_name):
            try:
                yield
            except Exception:
                LOGGER.exception("STEP FAIL | %s", step_name)
                if self._screenshot_after_steps:
                    self._capture_step_screenshot(step_name, "failure")
                raise
            else:
                LOGGER.info("STEP PASS | %s", step_name)
                if self._screenshot_after_steps:
                    self._capture_step_screenshot(step_name, "success")

    def capture_screenshot_step(self, name: str) -> None:
        """Create a dedicated Allure step containing a controlled screenshot."""

        step_name = name.strip()
        if not step_name:
            raise ValueError("step name must not be empty")

        LOGGER.info("STEP START | %s", step_name)
        with allure.step(step_name):
            try:
                self._capture_step_screenshot(step_name, "manual")
            except Exception:
                LOGGER.exception("STEP FAIL | %s", step_name)
                raise
            else:
                LOGGER.info("STEP PASS | %s", step_name)

    def open(self, url: str) -> None:
        """Navigate to an absolute URL or a path relative to ``base_url``."""

        if self._base_url and not url.startswith(("http://", "https://")):
            target_url = f"{self._base_url}/{url.lstrip('/')}"
        else:
            target_url = url
        LOGGER.info("OPEN URL | %s", target_url)
        try:
            self._driver.get(target_url)
        except TimeoutException:
            LOGGER.warning(
                "PAGE LOAD TIMEOUT | %s | continuing with the configured element visibility check",
                target_url,
                exc_info=True,
            )

    def page(self, page_type: type[PageType]) -> PageType:
        """Instantiate a page object using this client's driver and timeout."""

        LOGGER.info("CREATE PAGE OBJECT | %s", page_type.__name__)
        return page_type(self._driver, timeout=self._timeout)

    def _capture_step_screenshot(self, step_name: str, status: str) -> None:
        if not self._screenshots_enabled:
            LOGGER.info("STEP SCREENSHOT SKIP | %s | screenshot capability disabled", step_name)
            return

        try:
            screenshot = self._driver.get_screenshot_as_png()
        except Exception:
            LOGGER.warning(
                "STEP SCREENSHOT FAIL | %s | unable to capture browser screenshot",
                step_name,
                exc_info=True,
            )
            return

        try:
            allure.attach(
                screenshot,
                name=f"{status}-step-screenshot-{self._safe_filename(step_name)}",
                attachment_type=AttachmentType.PNG,
            )
        except Exception:
            LOGGER.warning(
                "STEP SCREENSHOT FAIL | %s | unable to attach screenshot to Allure",
                step_name,
                exc_info=True,
            )

        if self._screenshot_directory is None:
            return

        self._screenshot_sequence += 1
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        screenshot_name = (
            f"{timestamp}-{self._screenshot_sequence:04d}-"
            f"{status}-{self._safe_filename(step_name)}.png"
        )
        screenshot_path = self._screenshot_directory / screenshot_name
        try:
            self._screenshot_directory.mkdir(parents=True, exist_ok=True)
            screenshot_path.write_bytes(screenshot)
        except OSError:
            LOGGER.warning(
                "STEP SCREENSHOT FAIL | %s | unable to persist screenshot at %s",
                step_name,
                screenshot_path,
                exc_info=True,
            )

    @staticmethod
    def _safe_filename(value: str) -> str:
        return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "step"

    def close(self) -> None:
        """Close this client's browser session."""

        self._driver.quit()

    def quit(self) -> None:
        """Alias for :meth:`close` for WebDriver-oriented integrations."""

        self.close()

    def __enter__(self) -> "UIClient":
        return self

    def __exit__(self, _exc_type: object, _exc_value: object, _traceback: object) -> None:
        self.close()
