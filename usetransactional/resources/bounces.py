"""
Bounces Resource

Bounce management operations.
"""

from typing import Any, Dict, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import Bounce, BounceList


class Bounces(BaseResource):
    """Bounce management operations."""

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        bounce_type: Optional[str] = None,
        inactive: Optional[bool] = None,
        email_filter: Optional[str] = None,
        tag: Optional[str] = None,
        message_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> BounceList:
        """
        List bounces.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            bounce_type: Filter by bounce type
            inactive: Filter by inactive status
            email_filter: Filter by email address
            tag: Filter by tag
            message_id: Filter by message ID
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)

        Returns:
            BounceList with bounces and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if bounce_type:
            params["type"] = bounce_type
        if inactive is not None:
            params["inactive"] = inactive
        if email_filter:
            params["emailFilter"] = email_filter
        if tag:
            params["tag"] = tag
        if message_id:
            params["messageID"] = message_id
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date

        response = self._http.get("/bounces", params=params)
        return BounceList.model_validate(response)

    def get(self, bounce_id: int) -> Bounce:
        """
        Get a bounce by ID.

        Args:
            bounce_id: Bounce ID

        Returns:
            Bounce details
        """
        response = self._http.get(f"/bounces/{bounce_id}")
        return Bounce.model_validate(response)

    def activate(self, email: str) -> None:
        """
        Activate a bounced email (allow sending again).

        Args:
            email: Email address to activate
        """
        import urllib.parse
        encoded = urllib.parse.quote(email, safe="")
        self._http.put(f"/bounces/{encoded}/activate")


class AsyncBounces(AsyncBaseResource):
    """Asynchronous bounce management operations."""

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        bounce_type: Optional[str] = None,
        inactive: Optional[bool] = None,
        email_filter: Optional[str] = None,
        tag: Optional[str] = None,
        message_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> BounceList:
        """List bounces asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if bounce_type:
            params["type"] = bounce_type
        if inactive is not None:
            params["inactive"] = inactive
        if email_filter:
            params["emailFilter"] = email_filter
        if tag:
            params["tag"] = tag
        if message_id:
            params["messageID"] = message_id
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date

        response = await self._http.get("/bounces", params=params)
        return BounceList.model_validate(response)

    async def get(self, bounce_id: int) -> Bounce:
        """Get a bounce by ID asynchronously."""
        response = await self._http.get(f"/bounces/{bounce_id}")
        return Bounce.model_validate(response)

    async def activate(self, email: str) -> None:
        """Activate a bounced email asynchronously."""
        import urllib.parse
        encoded = urllib.parse.quote(email, safe="")
        await self._http.put(f"/bounces/{encoded}/activate")
