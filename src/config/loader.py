"""Load YAML configuration into framework dataclasses."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from models.configuration import FrameworkConfig
from project import DEFAULT_CONFIG_PATH, PROJECT_ROOT


def load_config(config_path: Path | None = None) -> FrameworkConfig:
    """Load a YAML configuration file after loading local environment variables."""
    load_dotenv(PROJECT_ROOT / ".env")
    selected_path = config_path or DEFAULT_CONFIG_PATH

    with selected_path.open(encoding="utf-8") as config_file:
        raw_values = yaml.safe_load(config_file) or {}

    if not isinstance(raw_values, dict):
        raise ValueError("The root of the YAML configuration must be a mapping.")

    values = _expand_environment_variables(raw_values)
    return FrameworkConfig.from_mapping(values, PROJECT_ROOT)


def _expand_environment_variables(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, dict):
        return {key: _expand_environment_variables(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_environment_variables(item) for item in value]
    return value
