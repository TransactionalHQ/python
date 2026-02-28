"""
HTTP Client

Low-level HTTP client for making API requests.
"""

import time
from typing import Any, Dict, Optional, TypeVar, Generic
from dataclasses import dataclass

import httpx

from usetransactional.errors import raise_for_status, RateLimitError, ServerError

T = TypeVar("T")

DEFAULT_BASE_URL = "https://api.usetransactional.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRIES = 3
SDK_VERSION = "0.1.0"


@dataclass
class RetryConfig:
    """Retry configuration."""

    max_retries: int = 3
    initial_delay: float = 0.5
    max_delay: float = 30.0
    backoff_factor: float = 2.0
    retry_on_status: tuple = (429, 500, 502, 503, 504)


class HttpClient:
    """Synchronous HTTP client for the Transactional API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retry_config: Optional[RetryConfig] = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig()

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"transactional-python/{SDK_VERSION}",
            },
        )

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Check if request should be retried."""
        if attempt >= self.retry_config.max_retries:
            return False
        return status_code in self.retry_config.retry_on_status

    def _get_retry_delay(self, attempt: int, retry_after: Optional[int] = None) -> float:
        """Calculate delay before next retry."""
        if retry_after:
            return float(retry_after)

        delay = self.retry_config.initial_delay * (
            self.retry_config.backoff_factor ** attempt
        )
        return min(delay, self.retry_config.max_delay)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic."""
        url = path if path.startswith("/") else f"/{path}"

        for attempt in range(self.retry_config.max_retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )

                # Parse response
                if response.status_code == 204:
                    return {}

                try:
                    data = response.json()
                except Exception:
                    data = {}

                # Check for errors
                if response.status_code >= 400:
                    if self._should_retry(response.status_code, attempt):
                        retry_after = response.headers.get("Retry-After")
                        delay = self._get_retry_delay(
                            attempt, int(retry_after) if retry_after else None
                        )
                        time.sleep(delay)
                        continue

                    raise_for_status(response.status_code, data)

                return data

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempt < self.retry_config.max_retries:
                    delay = self._get_retry_delay(attempt)
                    time.sleep(delay)
                    continue
                raise ServerError(
                    message=f"Request failed: {str(e)}",
                    code="NETWORK_ERROR",
                )

        # Should not reach here
        raise ServerError(message="Max retries exceeded")

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        return self._request("GET", path, params=params)

    def post(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request."""
        return self._request("POST", path, json=json)

    def put(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return self._request("PUT", path, json=json)

    def patch(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PATCH request."""
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return self._request("DELETE", path)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client for the Transactional API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retry_config: Optional[RetryConfig] = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retry_config = retry_config or RetryConfig()

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"transactional-python/{SDK_VERSION}",
            },
        )

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Check if request should be retried."""
        if attempt >= self.retry_config.max_retries:
            return False
        return status_code in self.retry_config.retry_on_status

    def _get_retry_delay(self, attempt: int, retry_after: Optional[int] = None) -> float:
        """Calculate delay before next retry."""
        if retry_after:
            return float(retry_after)

        delay = self.retry_config.initial_delay * (
            self.retry_config.backoff_factor ** attempt
        )
        return min(delay, self.retry_config.max_delay)

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic."""
        import asyncio

        url = path if path.startswith("/") else f"/{path}"

        for attempt in range(self.retry_config.max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                )

                # Parse response
                if response.status_code == 204:
                    return {}

                try:
                    data = response.json()
                except Exception:
                    data = {}

                # Check for errors
                if response.status_code >= 400:
                    if self._should_retry(response.status_code, attempt):
                        retry_after = response.headers.get("Retry-After")
                        delay = self._get_retry_delay(
                            attempt, int(retry_after) if retry_after else None
                        )
                        await asyncio.sleep(delay)
                        continue

                    raise_for_status(response.status_code, data)

                return data

            except (httpx.TimeoutException, httpx.NetworkError) as e:
                if attempt < self.retry_config.max_retries:
                    delay = self._get_retry_delay(attempt)
                    await asyncio.sleep(delay)
                    continue
                raise ServerError(
                    message=f"Request failed: {str(e)}",
                    code="NETWORK_ERROR",
                )

        # Should not reach here
        raise ServerError(message="Max retries exceeded")

    async def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make GET request."""
        return await self._request("GET", path, params=params)

    async def post(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make POST request."""
        return await self._request("POST", path, json=json)

    async def put(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return await self._request("PUT", path, json=json)

    async def patch(
        self, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make PATCH request."""
        return await self._request("PATCH", path, json=json)

    async def delete(self, path: str) -> Dict[str, Any]:
        """Make DELETE request."""
        return await self._request("DELETE", path)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
