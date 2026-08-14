"""Dataclass models for framework configuration."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from models.constants import (
    DEFAULT_ELEMENT_VISIBILITY_TIMEOUT_SECONDS,
    DEFAULT_EXPLICIT_TIMEOUT_SECONDS,
    DEFAULT_IMPLICIT_TIMEOUT_SECONDS,
    DEFAULT_PAGE_LOAD_TIMEOUT_SECONDS,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_SCRIPT_TIMEOUT_SECONDS,
)


@dataclass(frozen=True, slots=True)
class EnvironmentConfig:
    """Configuration for the application environment under test."""

    name: str
    base_url: str


@dataclass(frozen=True, slots=True)
class BrowserConfig:
    """Configuration for the first supported browser."""

    name: str = "chrome"
    headless: bool = False


@dataclass(frozen=True, slots=True)
class TimeoutConfig:
    """WebDriver and element-wait timeout values expressed in seconds."""

    implicit_seconds: int = DEFAULT_IMPLICIT_TIMEOUT_SECONDS
    explicit_seconds: int = DEFAULT_EXPLICIT_TIMEOUT_SECONDS
    element_visibility_seconds: int = DEFAULT_ELEMENT_VISIBILITY_TIMEOUT_SECONDS
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS
    page_load_seconds: int = DEFAULT_PAGE_LOAD_TIMEOUT_SECONDS
    script_seconds: int = DEFAULT_SCRIPT_TIMEOUT_SECONDS


@dataclass(frozen=True, slots=True)
class PathsConfig:
    """Project-relative paths used by framework features."""

    uploads: Path
    downloads: Path
    fixtures: Path
    allure_results: Path
    reports: Path
    logs: Path
    screenshots: Path


@dataclass(frozen=True, slots=True)
class EvidenceConfig:
    """Configuration for screenshot and report evidence capture."""

    screenshots_enabled: bool = True
    screenshot_after_steps: bool = False


@dataclass(frozen=True, slots=True)
class FrameworkConfig:
    """Complete configuration loaded from a YAML environment file."""

    environment: EnvironmentConfig
    browser: BrowserConfig
    timeouts: TimeoutConfig
    paths: PathsConfig
    evidence: EvidenceConfig

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any], project_root: Path) -> "FrameworkConfig":
        """Build a validated framework configuration from YAML values."""
        environment_values = _section(values, "environment")
        browser_values = _section(values, "browser")
        timeout_values = _section(values, "timeouts")
        path_values = _section(values, "paths")
        evidence_values = _optional_section(values, "evidence")

        environment = EnvironmentConfig(
            name=_required_string(environment_values, "name"),
            base_url=_required_string(environment_values, "base_url"),
        )
        browser = BrowserConfig(
            name=_optional_string(browser_values, "name", BrowserConfig.name),
            headless=_optional_bool(browser_values, "headless", BrowserConfig.headless),
        )
        timeouts = TimeoutConfig(
            implicit_seconds=_optional_non_negative_int(
                timeout_values,
                "implicit_seconds",
                DEFAULT_IMPLICIT_TIMEOUT_SECONDS,
            ),
            explicit_seconds=_optional_positive_int(
                timeout_values,
                "explicit_seconds",
                DEFAULT_EXPLICIT_TIMEOUT_SECONDS,
            ),
            element_visibility_seconds=_optional_positive_int(
                timeout_values,
                "element_visibility_seconds",
                DEFAULT_ELEMENT_VISIBILITY_TIMEOUT_SECONDS,
            ),
            poll_interval_seconds=_optional_positive_int(
                timeout_values,
                "poll_interval_seconds",
                DEFAULT_POLL_INTERVAL_SECONDS,
            ),
            page_load_seconds=_optional_positive_int(
                timeout_values,
                "page_load_seconds",
                DEFAULT_PAGE_LOAD_TIMEOUT_SECONDS,
            ),
            script_seconds=_optional_positive_int(
                timeout_values,
                "script_seconds",
                DEFAULT_SCRIPT_TIMEOUT_SECONDS,
            ),
        )
        paths = PathsConfig(
            uploads=_project_path(project_root, _required_string(path_values, "uploads")),
            downloads=_project_path(project_root, _required_string(path_values, "downloads")),
            fixtures=_project_path(project_root, _required_string(path_values, "fixtures")),
            allure_results=_project_path(
                project_root,
                _required_string(path_values, "allure_results"),
            ),
            reports=_project_path(project_root, _required_string(path_values, "reports")),
            logs=_project_path(project_root, _required_string(path_values, "logs")),
            screenshots=_project_path(project_root, _required_string(path_values, "screenshots")),
        )
        evidence = EvidenceConfig(
            screenshots_enabled=_optional_bool(
                evidence_values,
                "screenshots_enabled",
                EvidenceConfig.screenshots_enabled,
            ),
            screenshot_after_steps=_optional_bool(
                evidence_values,
                "screenshot_after_steps",
                EvidenceConfig.screenshot_after_steps,
            ),
        )

        return cls(
            environment=environment,
            browser=browser,
            timeouts=timeouts,
            paths=paths,
            evidence=evidence,
        )


def _section(values: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    section = values.get(name)
    if not isinstance(section, Mapping):
        raise ValueError(f"Configuration section '{name}' must be a mapping.")
    return section


def _optional_section(values: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    section = values.get(name, {})
    if not isinstance(section, Mapping):
        raise ValueError(f"Configuration section '{name}' must be a mapping.")
    return section


def _required_string(values: Mapping[str, Any], name: str) -> str:
    value = values.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Configuration value '{name}' must be a non-empty string.")
    return value


def _optional_string(values: Mapping[str, Any], name: str, default: str) -> str:
    value = values.get(name, default)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Configuration value '{name}' must be a non-empty string.")
    return value


def _optional_bool(values: Mapping[str, Any], name: str, default: bool) -> bool:
    value = values.get(name, default)
    if not isinstance(value, bool):
        raise ValueError(f"Configuration value '{name}' must be a boolean.")
    return value


def _optional_non_negative_int(values: Mapping[str, Any], name: str, default: int) -> int:
    value = values.get(name, default)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"Configuration value '{name}' must be a non-negative integer.")
    return value


def _optional_positive_int(values: Mapping[str, Any], name: str, default: int) -> int:
    value = values.get(name, default)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"Configuration value '{name}' must be a positive integer.")
    return value


def _project_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else project_root / path
