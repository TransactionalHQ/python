"""
Suppressions Resource

Email suppression list operations.
"""

from typing import Any, Dict, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import Suppression, SuppressionList, SuppressionCheckResult


class Suppressions(BaseResource):
    """Email suppression list operations."""

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        suppression_reason: Optional[str] = None,
        origin: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SuppressionList:
        """
        List suppressions.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            suppression_reason: Filter by reason
            origin: Filter by origin
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)

        Returns:
            SuppressionList with suppressions and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if suppression_reason:
            params["suppressionReason"] = suppression_reason
        if origin:
            params["origin"] = origin
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = self._http.get("/message-streams/outbound/suppressions/dump", params=params)
        return SuppressionList.model_validate(response)

    def check(self, email: str) -> SuppressionCheckResult:
        """
        Check if an email is suppressed.

        Args:
            email: Email address to check

        Returns:
            SuppressionCheckResult with suppression status
        """
        import urllib.parse
        encoded = urllib.parse.quote(email, safe="")
        response = self._http.get(f"/message-streams/outbound/suppressions/{encoded}")
        return SuppressionCheckResult.model_validate(response)

    def add(
        self,
        email: str,
        reason: str = "ManualSuppression",
    ) -> Suppression:
        """
        Add an email to the suppression list.

        Args:
            email: Email address to suppress
            reason: Suppression reason

        Returns:
            Created suppression entry
        """
        payload = {
            "Suppressions": [
                {
                    "EmailAddress": email,
                    "SuppressionReason": reason,
                }
            ]
        }
        response = self._http.post("/message-streams/outbound/suppressions", json=payload)
        return Suppression.model_validate(response["Suppressions"][0])

    def remove(self, email: str) -> None:
        """
        Remove an email from the suppression list.

        Args:
            email: Email address to remove
        """
        import urllib.parse
        encoded = urllib.parse.quote(email, safe="")
        self._http.delete(f"/message-streams/outbound/suppressions/delete/{encoded}")


class AsyncSuppressions(AsyncBaseResource):
    """Asynchronous email suppression list operations."""

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        suppression_reason: Optional[str] = None,
        origin: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SuppressionList:
        """List suppressions asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if suppression_reason:
            params["suppressionReason"] = suppression_reason
        if origin:
            params["origin"] = origin
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = await self._http.get("/message-streams/outbound/suppressions/dump", params=params)
        return SuppressionList.model_validate(response)

    async def check(self, email: str) -> SuppressionCheckResult:
        """Check if an email is suppressed asynchronously."""
        import urllib.parse
        encoded = urllib.parse.quote(email, safe="")
        response = await self._http.get(f"/message-streams/outbound/suppressions/{encoded}")
        return SuppressionCheckResult.model_validate(response)

    async def add(
        self,
        email: str,
        reason: str = "ManualSuppression",
    ) -> Suppression:
        """Add an email to the suppression list asynchronously."""
        payload = {
            "Suppressions": [
                {
                    "EmailAddress": email,
                    "SuppressionReason": reason,
                }
            ]
        }
        response = await self._http.post("/message-streams/outbound/suppressions", json=payload)
        return Suppression.model_validate(response["Suppressions"][0])

    async def remove(self, email: str) -> None:
        """Remove an email from the suppression list asynchronously."""
        import urllib.parse
        encoded = urllib.parse.quote(email, safe="")
        await self._http.delete(f"/message-streams/outbound/suppressions/delete/{encoded}")
