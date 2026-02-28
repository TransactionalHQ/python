"""
Transactional Client

Main client for interacting with the Transactional API.
"""

from typing import Optional

from usetransactional._http import (
    HttpClient,
    AsyncHttpClient,
    RetryConfig,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
)
from usetransactional.resources import (
    Emails,
    AsyncEmails,
    Templates,
    AsyncTemplates,
    Suppressions,
    AsyncSuppressions,
    Bounces,
    AsyncBounces,
    Messages,
    AsyncMessages,
    Stats,
    AsyncStats,
    Sms,
    AsyncSms,
    Forms,
    AsyncForms,
    Support,
    AsyncSupport,
)
from usetransactional.resources.auth import Auth


class Transactional:
    """
    Transactional API Client

    The main entry point for interacting with the Transactional API.

    Example:
        >>> from usetransactional import Transactional
        >>>
        >>> client = Transactional(api_key="tr_live_xxxxx")
        >>>
        >>> # Send an email
        >>> result = client.emails.send(
        ...     from_email="sender@domain.com",
        ...     to="recipient@example.com",
        ...     subject="Hello!",
        ...     html_body="<h1>Hello World</h1>",
        ... )
        >>>
        >>> print(result.message_id)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = 3,
    ) -> None:
        """
        Initialize the Transactional client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            retries: Number of automatic retries for failed requests
        """
        if not api_key:
            raise ValueError("API key is required")

        retry_config = RetryConfig(max_retries=retries)
        self._http = HttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            retry_config=retry_config,
        )

        # Email resources
        self.emails = Emails(self._http)
        self.templates = Templates(self._http)
        self.suppressions = Suppressions(self._http)
        self.bounces = Bounces(self._http)
        self.messages = Messages(self._http)
        self.stats = Stats(self._http)

        # SMS resources
        self.sms = Sms(self._http)

        # Auth resources
        self.auth = Auth(self._http)

        # Forms resources
        self.forms = Forms(self._http)

        # Support resources
        self.support = Support(self._http)

    def close(self) -> None:
        """Close the HTTP client."""
        self._http.close()

    def __enter__(self) -> "Transactional":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class AsyncTransactional:
    """
    Asynchronous Transactional API Client

    The async entry point for interacting with the Transactional API.

    Example:
        >>> import asyncio
        >>> from usetransactional import AsyncTransactional
        >>>
        >>> async def main():
        ...     client = AsyncTransactional(api_key="tr_live_xxxxx")
        ...
        ...     result = await client.emails.send(
        ...         from_email="sender@domain.com",
        ...         to="recipient@example.com",
        ...         subject="Hello!",
        ...         html_body="<h1>Hello World</h1>",
        ...     )
        ...
        ...     print(result.message_id)
        ...     await client.close()
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = 3,
    ) -> None:
        """
        Initialize the async Transactional client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            retries: Number of automatic retries for failed requests
        """
        if not api_key:
            raise ValueError("API key is required")

        retry_config = RetryConfig(max_retries=retries)
        self._http = AsyncHttpClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            retry_config=retry_config,
        )

        # Email resources
        self.emails = AsyncEmails(self._http)
        self.templates = AsyncTemplates(self._http)
        self.suppressions = AsyncSuppressions(self._http)
        self.bounces = AsyncBounces(self._http)
        self.messages = AsyncMessages(self._http)
        self.stats = AsyncStats(self._http)

        # SMS resources
        self.sms = AsyncSms(self._http)

        # Forms resources
        self.forms = AsyncForms(self._http)

        # Support resources
        self.support = AsyncSupport(self._http)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncTransactional":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
