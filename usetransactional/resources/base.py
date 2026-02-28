"""
Base Resource

Base class for all API resources.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from usetransactional._http import HttpClient, AsyncHttpClient


class BaseResource:
    """Base class for synchronous API resources."""

    def __init__(self, http: "HttpClient") -> None:
        self._http = http


class AsyncBaseResource:
    """Base class for asynchronous API resources."""

    def __init__(self, http: "AsyncHttpClient") -> None:
        self._http = http
