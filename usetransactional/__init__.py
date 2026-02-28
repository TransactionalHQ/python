"""
Transactional Python SDK

Official Python SDK for the Transactional API - Email, SMS, and Communication APIs.
"""

from usetransactional.client import Transactional, AsyncTransactional
from usetransactional.errors import (
    TransactionalError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    ServerError,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "Transactional",
    "AsyncTransactional",
    # Errors
    "TransactionalError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "ServerError",
    # Version
    "__version__",
]
