"""Project-root-relative paths shared by framework modules."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config"
DEFAULT_CONFIG_PATH = CONFIG_PATH / "default.yaml"
DATA_PATH = PROJECT_ROOT / "data"
UPLOADS_PATH = DATA_PATH / "uploads"
DOWNLOADS_PATH = DATA_PATH / "downloads"
FIXTURES_PATH = DATA_PATH / "fixtures"
REPORTS_PATH = PROJECT_ROOT / "allure-report"
LOGS_PATH = PROJECT_ROOT / "logs"
SCREENSHOTS_PATH = PROJECT_ROOT / "screenshots"
