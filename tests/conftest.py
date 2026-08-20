"""Shared pytest fixtures and Allure failure evidence for UI tests."""

import json
import logging
import shutil
from collections.abc import Generator
from contextlib import suppress
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.webdriver.remote.webdriver import WebDriver

from clients.ui_client import UIClient
from config.loader import load_config
from models.configuration import FrameworkConfig
from webdriver.factory import create_webdriver

PRESERVED_ARTIFACT_NAMES = frozenset({".gitkeep"})


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the supported browser-mode override."""

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser tests in headless Chrome mode.",
    )


def pytest_sessionstart(session: pytest.Session) -> None:
    """Remove generated test artifacts before pytest and Allure create new output."""

    del session
    config = load_config()
    for artifact_directory in (
        config.paths.downloads,
        config.paths.screenshots,
        config.paths.logs,
        config.paths.allure_results,
        config.paths.reports,
    ):
        clean_artifact_directory(artifact_directory)


@pytest.fixture(scope="session")
def config() -> FrameworkConfig:
    """Load the single test-environment configuration once per session."""

    return load_config()


@pytest.fixture(scope="session", autouse=True)
def execution_log_path(config: FrameworkConfig) -> Generator[Path, None, None]:
    """Configure one session file logger and expose its configured path."""

    config.paths.logs.mkdir(parents=True, exist_ok=True)
    log_path = config.paths.logs / "test-execution.log"
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    try:
        yield log_path
    finally:
        root_logger.removeHandler(file_handler)
        file_handler.close()


@pytest.fixture
def driver(
    request: pytest.FixtureRequest,
    config: FrameworkConfig,
) -> Generator[WebDriver, None, None]:
    """Create and tear down one configured local browser per test."""

    headless = bool(request.config.getoption("--headless")) or config.browser.headless
    browser = create_webdriver(
        config.browser.name,
        headless=headless,
        download_directory=config.paths.downloads,
    )
    browser.implicitly_wait(config.timeouts.implicit_seconds)
    browser.set_page_load_timeout(config.timeouts.page_load_seconds)
    browser.set_script_timeout(config.timeouts.script_seconds)
    yield browser
    browser.quit()


@pytest.fixture
def ui_client(driver: WebDriver, config: FrameworkConfig) -> UIClient:
    """Expose a high-level UI client to behavior-focused tests."""

    return UIClient(
        driver=driver,
        base_url=config.environment.base_url,
        screenshot_directory=config.paths.screenshots,
        timeout=config.timeouts.explicit_seconds,
        screenshots_enabled=config.evidence.screenshots_enabled,
        screenshot_after_steps=config.evidence.screenshot_after_steps,
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[object],
) -> Generator[None, None, None]:
    """Attach browser evidence when a test using the driver fails."""

    del call
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    execution_log = item.funcargs.get("execution_log_path")
    if isinstance(execution_log, Path):
        attach_execution_log(execution_log)

    browser = item.funcargs.get("driver")
    if not isinstance(browser, WebDriver):
        return

    attach_browser_evidence(browser)


def attach_execution_log(log_path: Path) -> None:
    """Attach the configured execution log to a failed Allure result."""

    with suppress(Exception):
        for handler in logging.getLogger().handlers:
            handler.flush()
        allure.attach.file(
            str(log_path),
            name="execution-log",
            attachment_type=AttachmentType.TEXT,
        )


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


def clean_artifact_directory(directory: Path) -> None:
    """Remove generated files from a configured artifact directory."""

    directory.mkdir(parents=True, exist_ok=True)
    for path in directory.iterdir():
        if path.name in PRESERVED_ARTIFACT_NAMES:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
