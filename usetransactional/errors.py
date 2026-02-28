"""
Transactional SDK Errors

Custom exception classes for API errors.
"""

from typing import Any, Optional


class TransactionalError(Exception):
    """Base exception for all Transactional SDK errors."""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class AuthenticationError(TransactionalError):
    """Raised when API authentication fails (401)."""

    def __init__(
        self,
        message: str = "Invalid or missing API key",
        code: str = "UNAUTHORIZED",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=401,
            details=details,
        )


class NotFoundError(TransactionalError):
    """Raised when a resource is not found (404)."""

    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=404,
            details=details,
        )


class ValidationError(TransactionalError):
    """Raised when request validation fails (400)."""

    def __init__(
        self,
        message: str = "Validation error",
        code: str = "VALIDATION_ERROR",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=400,
            details=details,
        )


class RateLimitError(TransactionalError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        code: str = "RATE_LIMITED",
        retry_after: Optional[int] = None,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=429,
            details=details,
        )
        self.retry_after = retry_after


class ServerError(TransactionalError):
    """Raised when server returns 5xx error."""

    def __init__(
        self,
        message: str = "Internal server error",
        code: str = "SERVER_ERROR",
        status_code: int = 500,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=status_code,
            details=details,
        )


def raise_for_status(status_code: int, response_data: dict) -> None:
    """Raise appropriate exception based on status code and response."""
    if status_code < 400:
        return

    error_data = response_data.get("error", {})
    message = error_data.get("message", "Unknown error")
    code = error_data.get("code", "UNKNOWN")
    details = error_data.get("details")

    if status_code == 401:
        raise AuthenticationError(message=message, code=code, details=details)
    elif status_code == 404:
        raise NotFoundError(message=message, code=code, details=details)
    elif status_code == 400:
        raise ValidationError(message=message, code=code, details=details)
    elif status_code == 429:
        retry_after = error_data.get("retryAfter")
        raise RateLimitError(
            message=message, code=code, retry_after=retry_after, details=details
        )
    elif status_code >= 500:
        raise ServerError(
            message=message, code=code, status_code=status_code, details=details
        )
    else:
        raise TransactionalError(
            message=message, code=code, status_code=status_code, details=details
        )
