"""
Stats Resource

Statistics operations.
"""

from typing import Any, Dict, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import StatsSummary, StatsOverview


class Stats(BaseResource):
    """Statistics operations."""

    def get_overview(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """
        Get statistics overview.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            tag: Filter by tag
            message_stream: Filter by message stream

        Returns:
            StatsOverview with daily statistics
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = self._http.get("/stats/outbound", params=params)
        return StatsOverview.model_validate(response)

    def get_sends(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """
        Get send statistics.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            tag: Filter by tag
            message_stream: Filter by message stream

        Returns:
            StatsOverview with daily send statistics
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = self._http.get("/stats/outbound/sends", params=params)
        return StatsOverview.model_validate(response)

    def get_bounces(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """
        Get bounce statistics.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            tag: Filter by tag
            message_stream: Filter by message stream

        Returns:
            StatsOverview with daily bounce statistics
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = self._http.get("/stats/outbound/bounces", params=params)
        return StatsOverview.model_validate(response)

    def get_opens(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """
        Get open statistics.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            tag: Filter by tag
            message_stream: Filter by message stream

        Returns:
            StatsOverview with daily open statistics
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = self._http.get("/stats/outbound/opens", params=params)
        return StatsOverview.model_validate(response)

    def get_clicks(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """
        Get click statistics.

        Args:
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            tag: Filter by tag
            message_stream: Filter by message stream

        Returns:
            StatsOverview with daily click statistics
        """
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = self._http.get("/stats/outbound/clicks", params=params)
        return StatsOverview.model_validate(response)


class AsyncStats(AsyncBaseResource):
    """Asynchronous statistics operations."""

    async def get_overview(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """Get statistics overview asynchronously."""
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = await self._http.get("/stats/outbound", params=params)
        return StatsOverview.model_validate(response)

    async def get_sends(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """Get send statistics asynchronously."""
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = await self._http.get("/stats/outbound/sends", params=params)
        return StatsOverview.model_validate(response)

    async def get_bounces(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """Get bounce statistics asynchronously."""
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = await self._http.get("/stats/outbound/bounces", params=params)
        return StatsOverview.model_validate(response)

    async def get_opens(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """Get open statistics asynchronously."""
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = await self._http.get("/stats/outbound/opens", params=params)
        return StatsOverview.model_validate(response)

    async def get_clicks(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        tag: Optional[str] = None,
        message_stream: Optional[str] = None,
    ) -> StatsOverview:
        """Get click statistics asynchronously."""
        params: Dict[str, Any] = {}
        if from_date:
            params["fromdate"] = from_date
        if to_date:
            params["todate"] = to_date
        if tag:
            params["tag"] = tag
        if message_stream:
            params["messagestream"] = message_stream

        response = await self._http.get("/stats/outbound/clicks", params=params)
        return StatsOverview.model_validate(response)
