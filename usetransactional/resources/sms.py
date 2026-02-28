"""
SMS Resource

SMS messaging operations.
"""

from typing import Any, Dict, List, Optional
import urllib.parse

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import (
    SmsSendResult,
    SmsMessage,
    SmsMessageList,
    InboundSmsMessageList,
    SmsSuppression,
    SmsSuppressionList,
    SmsSuppressionCheckResult,
    SmsWebhook,
    SmsTemplateList,
)


class SmsSuppressions(BaseResource):
    """SMS suppression (opt-out) list operations."""

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        reason: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SmsSuppressionList:
        """
        List SMS suppressions.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            reason: Filter by reason (OPT_OUT, MANUAL, CARRIER_BLOCK, INVALID_NUMBER)
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)

        Returns:
            SmsSuppressionList with suppressions and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if reason:
            params["reason"] = reason
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = self._http.get("/sms/suppressions", params=params)
        return SmsSuppressionList.model_validate(response)

    def check(self, phone_number: str) -> SmsSuppressionCheckResult:
        """
        Check if a phone number is suppressed.

        Args:
            phone_number: Phone number in E.164 format

        Returns:
            SmsSuppressionCheckResult with suppression status
        """
        encoded = urllib.parse.quote(phone_number, safe="")
        response = self._http.get(f"/sms/suppressions/check/{encoded}")
        return SmsSuppressionCheckResult.model_validate(response)

    def add(
        self,
        phone_number: str,
        reason: str = "MANUAL",
        notes: Optional[str] = None,
    ) -> SmsSuppression:
        """
        Add a phone number to the suppression list.

        Args:
            phone_number: Phone number in E.164 format
            reason: Suppression reason (MANUAL, OPT_OUT, etc.)
            notes: Optional notes

        Returns:
            Created suppression entry
        """
        payload: Dict[str, Any] = {
            "phoneNumber": phone_number,
            "reason": reason,
        }
        if notes:
            payload["notes"] = notes

        response = self._http.post("/sms/suppressions", json=payload)
        return SmsSuppression.model_validate(response)

    def remove(self, phone_number: str) -> None:
        """
        Remove a phone number from the suppression list.

        Args:
            phone_number: Phone number in E.164 format
        """
        encoded = urllib.parse.quote(phone_number, safe="")
        self._http.delete(f"/sms/suppressions/{encoded}")


class SmsWebhooks(BaseResource):
    """SMS webhook operations."""

    def list(self) -> List[SmsWebhook]:
        """
        List SMS webhooks.

        Returns:
            List of webhooks
        """
        response = self._http.get("/sms/webhooks")
        return [SmsWebhook.model_validate(w) for w in response]

    def get(self, webhook_id: str) -> SmsWebhook:
        """
        Get a webhook by ID.

        Args:
            webhook_id: Webhook ID

        Returns:
            Webhook details
        """
        response = self._http.get(f"/sms/webhooks/{webhook_id}")
        return SmsWebhook.model_validate(response)

    def create(
        self,
        url: str,
        events: List[str],
    ) -> SmsWebhook:
        """
        Create a webhook.

        Args:
            url: Webhook URL
            events: List of events to subscribe to

        Returns:
            Created webhook
        """
        payload = {
            "url": url,
            "events": events,
        }
        response = self._http.post("/sms/webhooks", json=payload)
        return SmsWebhook.model_validate(response)

    def update(
        self,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
    ) -> SmsWebhook:
        """
        Update a webhook.

        Args:
            webhook_id: Webhook ID
            url: New URL
            events: New events
            is_active: Active status

        Returns:
            Updated webhook
        """
        payload: Dict[str, Any] = {}
        if url:
            payload["url"] = url
        if events:
            payload["events"] = events
        if is_active is not None:
            payload["isActive"] = is_active

        response = self._http.patch(f"/sms/webhooks/{webhook_id}", json=payload)
        return SmsWebhook.model_validate(response)

    def delete(self, webhook_id: str) -> None:
        """
        Delete a webhook.

        Args:
            webhook_id: Webhook ID
        """
        self._http.delete(f"/sms/webhooks/{webhook_id}")


class SmsTemplates(BaseResource):
    """SMS template operations."""

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        category: Optional[str] = None,
    ) -> SmsTemplateList:
        """
        List available SMS templates.

        Args:
            count: Number to return
            offset: Pagination offset
            category: Filter by category

        Returns:
            SmsTemplateList with templates and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if category:
            params["category"] = category

        response = self._http.get("/sms/templates", params=params)
        return SmsTemplateList.model_validate(response)


class Sms(BaseResource):
    """SMS messaging operations."""

    def __init__(self, http: Any) -> None:
        super().__init__(http)
        self.suppressions = SmsSuppressions(http)
        self.webhooks = SmsWebhooks(http)
        self.templates = SmsTemplates(http)

    def send(
        self,
        to: str,
        template_alias: Optional[str] = None,
        template_id: Optional[int] = None,
        template_model: Optional[Dict[str, Any]] = None,
        tag: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> SmsSendResult:
        """
        Send a single SMS.

        Args:
            to: Recipient phone number in E.164 format
            template_alias: Pool template alias
            template_id: Pool template ID
            template_model: Variables for template substitution
            tag: Tag for categorization
            metadata: Custom metadata

        Returns:
            SmsSendResult with message ID and status
        """
        payload: Dict[str, Any] = {"to": to}
        if template_alias:
            payload["templateAlias"] = template_alias
        if template_id:
            payload["templateId"] = template_id
        if template_model:
            payload["templateModel"] = template_model
        if tag:
            payload["tag"] = tag
        if metadata:
            payload["metadata"] = metadata

        response = self._http.post("/sms", json=payload)
        return SmsSendResult.model_validate(response)

    def send_batch(
        self,
        messages: List[Dict[str, Any]],
    ) -> List[SmsSendResult]:
        """
        Send batch SMS (up to 500).

        Args:
            messages: List of message dicts with keys:
                - to: Recipient phone number
                - template_alias: Template alias
                - template_id: Template ID
                - template_model: Template variables
                - tag: Tag
                - metadata: Metadata

        Returns:
            List of SmsSendResult for each message
        """
        payloads = []
        for msg in messages:
            payload: Dict[str, Any] = {"to": msg["to"]}
            if msg.get("template_alias"):
                payload["templateAlias"] = msg["template_alias"]
            if msg.get("template_id"):
                payload["templateId"] = msg["template_id"]
            if msg.get("template_model"):
                payload["templateModel"] = msg["template_model"]
            if msg.get("tag"):
                payload["tag"] = msg["tag"]
            if msg.get("metadata"):
                payload["metadata"] = msg["metadata"]
            payloads.append(payload)

        response = self._http.post("/sms/batch", json=payloads)
        return [SmsSendResult.model_validate(r) for r in response]

    def get(self, message_id: str) -> SmsMessage:
        """
        Get SMS message details.

        Args:
            message_id: Message ID

        Returns:
            Full message details
        """
        response = self._http.get(f"/sms/{message_id}")
        return SmsMessage.model_validate(response)

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        status: Optional[str] = None,
        direction: Optional[str] = None,
        tag: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SmsMessageList:
        """
        List SMS messages.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            status: Filter by status
            direction: Filter by direction (OUTBOUND, INBOUND)
            tag: Filter by tag
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)

        Returns:
            SmsMessageList with messages and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if status:
            params["status"] = status
        if direction:
            params["direction"] = direction
        if tag:
            params["tag"] = tag
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = self._http.get("/sms/messages", params=params)
        return SmsMessageList.model_validate(response)

    def list_inbound(
        self,
        count: int = 100,
        offset: int = 0,
        from_number: Optional[str] = None,
        to_number: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> InboundSmsMessageList:
        """
        List inbound SMS messages.

        Args:
            count: Number to return (max 500)
            offset: Pagination offset
            from_number: Filter by sender number
            to_number: Filter by receiving number
            from_date: Filter by start date (ISO 8601)
            to_date: Filter by end date (ISO 8601)

        Returns:
            InboundSmsMessageList with messages and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if from_number:
            params["fromNumber"] = from_number
        if to_number:
            params["toNumber"] = to_number
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = self._http.get("/sms/inbound", params=params)
        return InboundSmsMessageList.model_validate(response)


# Async versions


class AsyncSmsSuppressions(AsyncBaseResource):
    """Asynchronous SMS suppression operations."""

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        reason: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SmsSuppressionList:
        """List SMS suppressions asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if reason:
            params["reason"] = reason
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = await self._http.get("/sms/suppressions", params=params)
        return SmsSuppressionList.model_validate(response)

    async def check(self, phone_number: str) -> SmsSuppressionCheckResult:
        """Check if a phone number is suppressed asynchronously."""
        encoded = urllib.parse.quote(phone_number, safe="")
        response = await self._http.get(f"/sms/suppressions/check/{encoded}")
        return SmsSuppressionCheckResult.model_validate(response)

    async def add(
        self,
        phone_number: str,
        reason: str = "MANUAL",
        notes: Optional[str] = None,
    ) -> SmsSuppression:
        """Add a phone number to the suppression list asynchronously."""
        payload: Dict[str, Any] = {
            "phoneNumber": phone_number,
            "reason": reason,
        }
        if notes:
            payload["notes"] = notes

        response = await self._http.post("/sms/suppressions", json=payload)
        return SmsSuppression.model_validate(response)

    async def remove(self, phone_number: str) -> None:
        """Remove a phone number from the suppression list asynchronously."""
        encoded = urllib.parse.quote(phone_number, safe="")
        await self._http.delete(f"/sms/suppressions/{encoded}")


class AsyncSmsWebhooks(AsyncBaseResource):
    """Asynchronous SMS webhook operations."""

    async def list(self) -> List[SmsWebhook]:
        """List SMS webhooks asynchronously."""
        response = await self._http.get("/sms/webhooks")
        return [SmsWebhook.model_validate(w) for w in response]

    async def get(self, webhook_id: str) -> SmsWebhook:
        """Get a webhook by ID asynchronously."""
        response = await self._http.get(f"/sms/webhooks/{webhook_id}")
        return SmsWebhook.model_validate(response)

    async def create(
        self,
        url: str,
        events: List[str],
    ) -> SmsWebhook:
        """Create a webhook asynchronously."""
        payload = {
            "url": url,
            "events": events,
        }
        response = await self._http.post("/sms/webhooks", json=payload)
        return SmsWebhook.model_validate(response)

    async def update(
        self,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
    ) -> SmsWebhook:
        """Update a webhook asynchronously."""
        payload: Dict[str, Any] = {}
        if url:
            payload["url"] = url
        if events:
            payload["events"] = events
        if is_active is not None:
            payload["isActive"] = is_active

        response = await self._http.patch(f"/sms/webhooks/{webhook_id}", json=payload)
        return SmsWebhook.model_validate(response)

    async def delete(self, webhook_id: str) -> None:
        """Delete a webhook asynchronously."""
        await self._http.delete(f"/sms/webhooks/{webhook_id}")


class AsyncSmsTemplates(AsyncBaseResource):
    """Asynchronous SMS template operations."""

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        category: Optional[str] = None,
    ) -> SmsTemplateList:
        """List available SMS templates asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if category:
            params["category"] = category

        response = await self._http.get("/sms/templates", params=params)
        return SmsTemplateList.model_validate(response)


class AsyncSms(AsyncBaseResource):
    """Asynchronous SMS messaging operations."""

    def __init__(self, http: Any) -> None:
        super().__init__(http)
        self.suppressions = AsyncSmsSuppressions(http)
        self.webhooks = AsyncSmsWebhooks(http)
        self.templates = AsyncSmsTemplates(http)

    async def send(
        self,
        to: str,
        template_alias: Optional[str] = None,
        template_id: Optional[int] = None,
        template_model: Optional[Dict[str, Any]] = None,
        tag: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> SmsSendResult:
        """Send a single SMS asynchronously."""
        payload: Dict[str, Any] = {"to": to}
        if template_alias:
            payload["templateAlias"] = template_alias
        if template_id:
            payload["templateId"] = template_id
        if template_model:
            payload["templateModel"] = template_model
        if tag:
            payload["tag"] = tag
        if metadata:
            payload["metadata"] = metadata

        response = await self._http.post("/sms", json=payload)
        return SmsSendResult.model_validate(response)

    async def send_batch(
        self,
        messages: List[Dict[str, Any]],
    ) -> List[SmsSendResult]:
        """Send batch SMS asynchronously."""
        payloads = []
        for msg in messages:
            payload: Dict[str, Any] = {"to": msg["to"]}
            if msg.get("template_alias"):
                payload["templateAlias"] = msg["template_alias"]
            if msg.get("template_id"):
                payload["templateId"] = msg["template_id"]
            if msg.get("template_model"):
                payload["templateModel"] = msg["template_model"]
            if msg.get("tag"):
                payload["tag"] = msg["tag"]
            if msg.get("metadata"):
                payload["metadata"] = msg["metadata"]
            payloads.append(payload)

        response = await self._http.post("/sms/batch", json=payloads)
        return [SmsSendResult.model_validate(r) for r in response]

    async def get(self, message_id: str) -> SmsMessage:
        """Get SMS message details asynchronously."""
        response = await self._http.get(f"/sms/{message_id}")
        return SmsMessage.model_validate(response)

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        status: Optional[str] = None,
        direction: Optional[str] = None,
        tag: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> SmsMessageList:
        """List SMS messages asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if status:
            params["status"] = status
        if direction:
            params["direction"] = direction
        if tag:
            params["tag"] = tag
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = await self._http.get("/sms/messages", params=params)
        return SmsMessageList.model_validate(response)

    async def list_inbound(
        self,
        count: int = 100,
        offset: int = 0,
        from_number: Optional[str] = None,
        to_number: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> InboundSmsMessageList:
        """List inbound SMS messages asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if from_number:
            params["fromNumber"] = from_number
        if to_number:
            params["toNumber"] = to_number
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date

        response = await self._http.get("/sms/inbound", params=params)
        return InboundSmsMessageList.model_validate(response)
