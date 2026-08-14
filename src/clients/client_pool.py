"""Lifecycle management for multiple named UI clients."""

from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from clients.ui_client import UIClient


class UIClientPool:
    """Manage independently owned UI clients by a caller-provided name."""

    def __init__(self) -> None:
        self._clients: dict[str, UIClient] = {}

    def acquire(
        self,
        client_id: str,
        *,
        driver: WebDriver | None = None,
        browser: str = "chrome",
        headless: bool = False,
        download_directory: Path | str | None = None,
        screenshot_directory: Path | str | None = None,
        driver_path: Path | str | None = None,
        base_url: str | None = None,
        timeout: float = 10.0,
        screenshots_enabled: bool = True,
        screenshot_after_steps: bool = True,
    ) -> UIClient:
        """Create and register a new named client, rejecting duplicate names."""

        normalized_id = client_id.strip()
        if not normalized_id:
            raise ValueError("client_id must not be empty")
        if normalized_id in self._clients:
            raise ValueError(f"A client named {normalized_id!r} is already registered.")

        client = UIClient(
            driver,
            browser=browser,
            headless=headless,
            download_directory=download_directory,
            screenshot_directory=screenshot_directory,
            driver_path=driver_path,
            base_url=base_url,
            timeout=timeout,
            screenshots_enabled=screenshots_enabled,
            screenshot_after_steps=screenshot_after_steps,
        )
        self._clients[normalized_id] = client
        return client

    def get(self, client_id: str) -> UIClient:
        """Return a registered client or raise a clear lookup error."""

        try:
            return self._clients[client_id]
        except KeyError as error:
            raise KeyError(f"No UI client named {client_id!r} is registered.") from error

    def release(self, client_id: str) -> None:
        """Close and remove one registered client."""

        client = self._clients.pop(client_id)
        client.close()

    def close_all(self) -> None:
        """Close and remove every registered client."""

        clients = tuple(self._clients.values())
        self._clients.clear()
        for client in clients:
            client.close()

    def __len__(self) -> int:
        return len(self._clients)

    def __enter__(self) -> "UIClientPool":
        return self

    def __exit__(self, _exc_type: object, _exc_value: object, _traceback: object) -> None:
        self.close_all()
