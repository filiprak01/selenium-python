"""Chrome-specific Selenium option construction."""

from collections.abc import Sequence
from pathlib import Path

from selenium.webdriver.chrome.options import Options


def build_chrome_options(
    *,
    headless: bool = False,
    download_directory: Path | str | None = None,
    extra_arguments: Sequence[str] = (),
) -> Options:
    """Build Chrome options without creating a browser session."""

    options = Options()
    if headless:
        options.add_argument("--headless=new")

    for argument in extra_arguments:
        options.add_argument(argument)

    if download_directory is not None:
        download_path = Path(download_directory).expanduser().resolve()
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(download_path),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
            },
        )

    return options
