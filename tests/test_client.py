"""Tests for the Transactional client."""

import pytest
from usetransactional import Transactional, AsyncTransactional
from usetransactional.errors import TransactionalError


def test_client_requires_api_key():
    """Test that client raises error without API key."""
    with pytest.raises(ValueError, match="API key is required"):
        Transactional(api_key="")


def test_async_client_requires_api_key():
    """Test that async client raises error without API key."""
    with pytest.raises(ValueError, match="API key is required"):
        AsyncTransactional(api_key="")


def test_client_initialization():
    """Test client initializes with all resources."""
    client = Transactional(api_key="test_key")

    # Email resources
    assert hasattr(client, "emails")
    assert hasattr(client, "templates")
    assert hasattr(client, "suppressions")
    assert hasattr(client, "bounces")
    assert hasattr(client, "messages")
    assert hasattr(client, "stats")

    # SMS resources
    assert hasattr(client, "sms")
    assert hasattr(client.sms, "suppressions")
    assert hasattr(client.sms, "webhooks")
    assert hasattr(client.sms, "templates")

    client.close()


def test_client_context_manager():
    """Test client works as context manager."""
    with Transactional(api_key="test_key") as client:
        assert hasattr(client, "emails")


@pytest.mark.asyncio
async def test_async_client_context_manager():
    """Test async client works as context manager."""
    async with AsyncTransactional(api_key="test_key") as client:
        assert hasattr(client, "emails")
