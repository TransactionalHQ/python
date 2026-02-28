"""
Messages Resource

Message history operations.
"""

from typing import Any, Dict, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import EmailMessage, EmailMessageList


class Messages(BaseResource):
    """Message history operations."""

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        recipient: Optional[str] = None,
        from_email: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> EmailMessageList:
        """
        List sent messages.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            recipient: Filter by recipient
            from_email: Filter by sender
            tag: Filter by tag
            status: Filter by status
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)
            message_stream: Filter by message stream

        Returns:
            EmailMessageList with messages and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if recipient:
            params["recipient"] = recipient
        if from_email:
            params["fromemail"] = from_email
        if tag:
            params["tag"] = tag
        if status:
            params["status"] = status
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if message_stream:
            params["messagestream"] = message_stream

        response = self._http.get("/messages/outbound", params=params)
        return EmailMessageList.model_validate(response)

    def get(self, message_id: str) -> EmailMessage:
        """
        Get message details by ID.

        Args:
            message_id: Message ID

        Returns:
            Full message details
        """
        response = self._http.get(f"/messages/outbound/{message_id}/details")
        return EmailMessage.model_validate(response)

    def get_dump(self, message_id: str) -> str:
        """
        Get raw message dump.

        Args:
            message_id: Message ID

        Returns:
            Raw message content
        """
        response = self._http.get(f"/messages/outbound/{message_id}/dump")
        return response.get("Body", "")

    def list_inbound(
        self,
        count: int = 100,
        offset: int = 0,
        recipient: Optional[str] = None,
        from_email: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> EmailMessageList:
        """
        List inbound messages.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            recipient: Filter by recipient
            from_email: Filter by sender
            tag: Filter by tag
            status: Filter by status
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)

        Returns:
            EmailMessageList with messages and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if recipient:
            params["recipient"] = recipient
        if from_email:
            params["fromemail"] = from_email
        if tag:
            params["tag"] = tag
        if status:
            params["status"] = status
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date

        response = self._http.get("/messages/inbound", params=params)
        return EmailMessageList.model_validate(response)


class AsyncMessages(AsyncBaseResource):
    """Asynchronous message history operations."""

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        recipient: Optional[str] = None,
        from_email: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> EmailMessageList:
        """List sent messages asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if recipient:
            params["recipient"] = recipient
        if from_email:
            params["fromemail"] = from_email
        if tag:
            params["tag"] = tag
        if status:
            params["status"] = status
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if message_stream:
            params["messagestream"] = message_stream

        response = await self._http.get("/messages/outbound", params=params)
        return EmailMessageList.model_validate(response)

    async def get(self, message_id: str) -> EmailMessage:
        """Get message details by ID asynchronously."""
        response = await self._http.get(f"/messages/outbound/{message_id}/details")
        return EmailMessage.model_validate(response)

    async def get_dump(self, message_id: str) -> str:
        """Get raw message dump asynchronously."""
        response = await self._http.get(f"/messages/outbound/{message_id}/dump")
        return response.get("Body", "")

    async def list_inbound(
        self,
        count: int = 100,
        offset: int = 0,
        recipient: Optional[str] = None,
        from_email: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> EmailMessageList:
        """List inbound messages asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if recipient:
            params["recipient"] = recipient
        if from_email:
            params["fromemail"] = from_email
        if tag:
            params["tag"] = tag
        if status:
            params["status"] = status
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date

        response = await self._http.get("/messages/inbound", params=params)
        return EmailMessageList.model_validate(response)
