"""
Forms Resource

Forms and submissions operations.
"""

from typing import Any, Dict, List, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import (
    Form,
    FormList,
    FormField,
    FormSubmission,
    FormSubmissionList,
    FormAnalyticsResponse,
    FormWebhook,
)


class FormFields(BaseResource):
    """Form fields operations."""

    def create(
        self,
        form_id: int,
        field_type: str,
        label: str,
        placeholder: Optional[str] = None,
        help_text: Optional[str] = None,
        required: bool = False,
        order: Optional[int] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> FormField:
        """
        Add a field to a form.

        Args:
            form_id: Form ID
            field_type: Field type (SHORT_TEXT, EMAIL, etc.)
            label: Field label
            placeholder: Placeholder text
            help_text: Help text
            required: Is required
            order: Display order
            settings: Field settings

        Returns:
            Created field
        """
        payload: Dict[str, Any] = {
            "type": field_type,
            "label": label,
        }
        if placeholder:
            payload["placeholder"] = placeholder
        if help_text:
            payload["helpText"] = help_text
        if required:
            payload["required"] = required
        if order is not None:
            payload["order"] = order
        if settings:
            payload["settings"] = settings

        response = self._http.post(f"/forms/{form_id}/fields", json=payload)
        return FormField.model_validate(response)

    def update(
        self,
        form_id: int,
        field_id: int,
        label: Optional[str] = None,
        placeholder: Optional[str] = None,
        help_text: Optional[str] = None,
        required: Optional[bool] = None,
        order: Optional[int] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> FormField:
        """
        Update a form field.

        Args:
            form_id: Form ID
            field_id: Field ID
            label: Field label
            placeholder: Placeholder text
            help_text: Help text
            required: Is required
            order: Display order
            settings: Field settings

        Returns:
            Updated field
        """
        payload: Dict[str, Any] = {}
        if label:
            payload["label"] = label
        if placeholder:
            payload["placeholder"] = placeholder
        if help_text:
            payload["helpText"] = help_text
        if required is not None:
            payload["required"] = required
        if order is not None:
            payload["order"] = order
        if settings:
            payload["settings"] = settings

        response = self._http.put(f"/forms/{form_id}/fields/{field_id}", json=payload)
        return FormField.model_validate(response)

    def delete(self, form_id: int, field_id: int) -> None:
        """
        Delete a form field.

        Args:
            form_id: Form ID
            field_id: Field ID
        """
        self._http.delete(f"/forms/{form_id}/fields/{field_id}")

    def reorder(self, form_id: int, field_order: List[int]) -> None:
        """
        Reorder form fields.

        Args:
            form_id: Form ID
            field_order: Ordered list of field IDs
        """
        self._http.post(f"/forms/{form_id}/fields/reorder", json={"fieldOrder": field_order})


class FormSubmissions(BaseResource):
    """Form submissions operations."""

    def list(
        self,
        form_id: int,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> FormSubmissionList:
        """
        List form submissions.

        Args:
            form_id: Form ID
            page: Page number
            limit: Items per page
            status: Filter by status (PARTIAL, COMPLETE)
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            FormSubmissionList with submissions and pagination
        """
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if status:
            params["status"] = status
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = self._http.get(f"/forms/{form_id}/submissions", params=params)
        return FormSubmissionList.model_validate(response)

    def get(self, form_id: int, submission_id: int) -> FormSubmission:
        """
        Get a submission by ID.

        Args:
            form_id: Form ID
            submission_id: Submission ID

        Returns:
            Submission details
        """
        response = self._http.get(f"/forms/{form_id}/submissions/{submission_id}")
        return FormSubmission.model_validate(response)

    def delete(self, form_id: int, submission_id: int) -> None:
        """
        Delete a submission.

        Args:
            form_id: Form ID
            submission_id: Submission ID
        """
        self._http.delete(f"/forms/{form_id}/submissions/{submission_id}")

    def export(
        self,
        form_id: int,
        format: str = "csv",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
        """
        Export submissions.

        Args:
            form_id: Form ID
            format: Export format (csv, json)
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            Export data as string
        """
        params: Dict[str, Any] = {"format": format}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        return self._http.get(f"/forms/{form_id}/submissions/export", params=params)


class FormAnalytics(BaseResource):
    """Form analytics operations."""

    def get(
        self,
        form_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: str = "day",
    ) -> FormAnalyticsResponse:
        """
        Get form analytics.

        Args:
            form_id: Form ID
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)
            group_by: Group by period (day, week, month)

        Returns:
            Analytics data with summary and time series
        """
        params: Dict[str, Any] = {"groupBy": group_by}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = self._http.get(f"/forms/{form_id}/analytics", params=params)
        return FormAnalyticsResponse.model_validate(response)


class FormWebhooks(BaseResource):
    """Form webhooks operations."""

    def list(self, form_id: int) -> List[FormWebhook]:
        """
        List form webhooks.

        Args:
            form_id: Form ID

        Returns:
            List of webhooks
        """
        response = self._http.get(f"/forms/{form_id}/webhooks")
        return [FormWebhook.model_validate(w) for w in response]

    def create(
        self,
        form_id: int,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
    ) -> FormWebhook:
        """
        Create a webhook.

        Args:
            form_id: Form ID
            url: Webhook URL
            events: Events to subscribe to
            secret: Webhook secret

        Returns:
            Created webhook
        """
        payload: Dict[str, Any] = {
            "url": url,
            "events": events,
        }
        if secret:
            payload["secret"] = secret

        response = self._http.post(f"/forms/{form_id}/webhooks", json=payload)
        return FormWebhook.model_validate(response)

    def update(
        self,
        form_id: int,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
    ) -> FormWebhook:
        """
        Update a webhook.

        Args:
            form_id: Form ID
            webhook_id: Webhook ID
            url: Webhook URL
            events: Events to subscribe to
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

        response = self._http.put(f"/forms/{form_id}/webhooks/{webhook_id}", json=payload)
        return FormWebhook.model_validate(response)

    def delete(self, form_id: int, webhook_id: str) -> None:
        """
        Delete a webhook.

        Args:
            form_id: Form ID
            webhook_id: Webhook ID
        """
        self._http.delete(f"/forms/{form_id}/webhooks/{webhook_id}")


class Forms(BaseResource):
    """Forms operations."""

    def __init__(self, http: Any) -> None:
        super().__init__(http)
        self.fields = FormFields(http)
        self.submissions = FormSubmissions(http)
        self.analytics = FormAnalytics(http)
        self.webhooks = FormWebhooks(http)

    def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> FormList:
        """
        List forms.

        Args:
            page: Page number
            limit: Items per page
            status: Filter by status (DRAFT, LIVE, etc.)
            search: Search by title

        Returns:
            FormList with forms and pagination
        """
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if status:
            params["status"] = status
        if search:
            params["search"] = search

        response = self._http.get("/forms", params=params)
        return FormList.model_validate(response)

    def get(self, form_id: int) -> Form:
        """
        Get a form by ID.

        Args:
            form_id: Form ID

        Returns:
            Form details
        """
        response = self._http.get(f"/forms/{form_id}")
        return Form.model_validate(response)

    def create(
        self,
        title: str,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        theme: Optional[Dict[str, Any]] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
    ) -> Form:
        """
        Create a form.

        Args:
            title: Form title
            slug: Form slug
            description: Form description
            settings: Form settings
            theme: Form theme
            fields: Initial fields

        Returns:
            Created form
        """
        payload: Dict[str, Any] = {"title": title}
        if slug:
            payload["slug"] = slug
        if description:
            payload["description"] = description
        if settings:
            payload["settings"] = settings
        if theme:
            payload["theme"] = theme
        if fields:
            payload["fields"] = fields

        response = self._http.post("/forms", json=payload)
        return Form.model_validate(response)

    def update(
        self,
        form_id: int,
        title: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        theme: Optional[Dict[str, Any]] = None,
    ) -> Form:
        """
        Update a form.

        Args:
            form_id: Form ID
            title: Form title
            slug: Form slug
            description: Form description
            settings: Form settings
            theme: Form theme

        Returns:
            Updated form
        """
        payload: Dict[str, Any] = {}
        if title:
            payload["title"] = title
        if slug:
            payload["slug"] = slug
        if description:
            payload["description"] = description
        if settings:
            payload["settings"] = settings
        if theme:
            payload["theme"] = theme

        response = self._http.put(f"/forms/{form_id}", json=payload)
        return Form.model_validate(response)

    def delete(self, form_id: int) -> None:
        """
        Delete (archive) a form.

        Args:
            form_id: Form ID
        """
        self._http.delete(f"/forms/{form_id}")

    def publish(self, form_id: int) -> Form:
        """
        Publish a form.

        Args:
            form_id: Form ID

        Returns:
            Published form
        """
        response = self._http.post(f"/forms/{form_id}/publish")
        return Form.model_validate(response)

    def unpublish(self, form_id: int) -> Form:
        """
        Unpublish a form.

        Args:
            form_id: Form ID

        Returns:
            Unpublished form
        """
        response = self._http.post(f"/forms/{form_id}/unpublish")
        return Form.model_validate(response)

    def duplicate(self, form_id: int) -> Form:
        """
        Duplicate a form.

        Args:
            form_id: Form ID

        Returns:
            Duplicated form
        """
        response = self._http.post(f"/forms/{form_id}/duplicate")
        return Form.model_validate(response)


# Async versions


class AsyncFormFields(AsyncBaseResource):
    """Asynchronous form fields operations."""

    async def create(
        self,
        form_id: int,
        field_type: str,
        label: str,
        placeholder: Optional[str] = None,
        help_text: Optional[str] = None,
        required: bool = False,
        order: Optional[int] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> FormField:
        """Add a field to a form asynchronously."""
        payload: Dict[str, Any] = {
            "type": field_type,
            "label": label,
        }
        if placeholder:
            payload["placeholder"] = placeholder
        if help_text:
            payload["helpText"] = help_text
        if required:
            payload["required"] = required
        if order is not None:
            payload["order"] = order
        if settings:
            payload["settings"] = settings

        response = await self._http.post(f"/forms/{form_id}/fields", json=payload)
        return FormField.model_validate(response)

    async def update(
        self,
        form_id: int,
        field_id: int,
        label: Optional[str] = None,
        placeholder: Optional[str] = None,
        help_text: Optional[str] = None,
        required: Optional[bool] = None,
        order: Optional[int] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> FormField:
        """Update a form field asynchronously."""
        payload: Dict[str, Any] = {}
        if label:
            payload["label"] = label
        if placeholder:
            payload["placeholder"] = placeholder
        if help_text:
            payload["helpText"] = help_text
        if required is not None:
            payload["required"] = required
        if order is not None:
            payload["order"] = order
        if settings:
            payload["settings"] = settings

        response = await self._http.put(f"/forms/{form_id}/fields/{field_id}", json=payload)
        return FormField.model_validate(response)

    async def delete(self, form_id: int, field_id: int) -> None:
        """Delete a form field asynchronously."""
        await self._http.delete(f"/forms/{form_id}/fields/{field_id}")

    async def reorder(self, form_id: int, field_order: List[int]) -> None:
        """Reorder form fields asynchronously."""
        await self._http.post(f"/forms/{form_id}/fields/reorder", json={"fieldOrder": field_order})


class AsyncFormSubmissions(AsyncBaseResource):
    """Asynchronous form submissions operations."""

    async def list(
        self,
        form_id: int,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> FormSubmissionList:
        """List form submissions asynchronously."""
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if status:
            params["status"] = status
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = await self._http.get(f"/forms/{form_id}/submissions", params=params)
        return FormSubmissionList.model_validate(response)

    async def get(self, form_id: int, submission_id: int) -> FormSubmission:
        """Get a submission by ID asynchronously."""
        response = await self._http.get(f"/forms/{form_id}/submissions/{submission_id}")
        return FormSubmission.model_validate(response)

    async def delete(self, form_id: int, submission_id: int) -> None:
        """Delete a submission asynchronously."""
        await self._http.delete(f"/forms/{form_id}/submissions/{submission_id}")

    async def export(
        self,
        form_id: int,
        format: str = "csv",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
        """Export submissions asynchronously."""
        params: Dict[str, Any] = {"format": format}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        return await self._http.get(f"/forms/{form_id}/submissions/export", params=params)


class AsyncFormAnalytics(AsyncBaseResource):
    """Asynchronous form analytics operations."""

    async def get(
        self,
        form_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: str = "day",
    ) -> FormAnalyticsResponse:
        """Get form analytics asynchronously."""
        params: Dict[str, Any] = {"groupBy": group_by}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = await self._http.get(f"/forms/{form_id}/analytics", params=params)
        return FormAnalyticsResponse.model_validate(response)


class AsyncFormWebhooks(AsyncBaseResource):
    """Asynchronous form webhooks operations."""

    async def list(self, form_id: int) -> List[FormWebhook]:
        """List form webhooks asynchronously."""
        response = await self._http.get(f"/forms/{form_id}/webhooks")
        return [FormWebhook.model_validate(w) for w in response]

    async def create(
        self,
        form_id: int,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
    ) -> FormWebhook:
        """Create a webhook asynchronously."""
        payload: Dict[str, Any] = {
            "url": url,
            "events": events,
        }
        if secret:
            payload["secret"] = secret

        response = await self._http.post(f"/forms/{form_id}/webhooks", json=payload)
        return FormWebhook.model_validate(response)

    async def update(
        self,
        form_id: int,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
    ) -> FormWebhook:
        """Update a webhook asynchronously."""
        payload: Dict[str, Any] = {}
        if url:
            payload["url"] = url
        if events:
            payload["events"] = events
        if is_active is not None:
            payload["isActive"] = is_active

        response = await self._http.put(f"/forms/{form_id}/webhooks/{webhook_id}", json=payload)
        return FormWebhook.model_validate(response)

    async def delete(self, form_id: int, webhook_id: str) -> None:
        """Delete a webhook asynchronously."""
        await self._http.delete(f"/forms/{form_id}/webhooks/{webhook_id}")


class AsyncForms(AsyncBaseResource):
    """Asynchronous forms operations."""

    def __init__(self, http: Any) -> None:
        super().__init__(http)
        self.fields = AsyncFormFields(http)
        self.submissions = AsyncFormSubmissions(http)
        self.analytics = AsyncFormAnalytics(http)
        self.webhooks = AsyncFormWebhooks(http)

    async def list(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> FormList:
        """List forms asynchronously."""
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if status:
            params["status"] = status
        if search:
            params["search"] = search

        response = await self._http.get("/forms", params=params)
        return FormList.model_validate(response)

    async def get(self, form_id: int) -> Form:
        """Get a form by ID asynchronously."""
        response = await self._http.get(f"/forms/{form_id}")
        return Form.model_validate(response)

    async def create(
        self,
        title: str,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        theme: Optional[Dict[str, Any]] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
    ) -> Form:
        """Create a form asynchronously."""
        payload: Dict[str, Any] = {"title": title}
        if slug:
            payload["slug"] = slug
        if description:
            payload["description"] = description
        if settings:
            payload["settings"] = settings
        if theme:
            payload["theme"] = theme
        if fields:
            payload["fields"] = fields

        response = await self._http.post("/forms", json=payload)
        return Form.model_validate(response)

    async def update(
        self,
        form_id: int,
        title: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        theme: Optional[Dict[str, Any]] = None,
    ) -> Form:
        """Update a form asynchronously."""
        payload: Dict[str, Any] = {}
        if title:
            payload["title"] = title
        if slug:
            payload["slug"] = slug
        if description:
            payload["description"] = description
        if settings:
            payload["settings"] = settings
        if theme:
            payload["theme"] = theme

        response = await self._http.put(f"/forms/{form_id}", json=payload)
        return Form.model_validate(response)

    async def delete(self, form_id: int) -> None:
        """Delete (archive) a form asynchronously."""
        await self._http.delete(f"/forms/{form_id}")

    async def publish(self, form_id: int) -> Form:
        """Publish a form asynchronously."""
        response = await self._http.post(f"/forms/{form_id}/publish")
        return Form.model_validate(response)

    async def unpublish(self, form_id: int) -> Form:
        """Unpublish a form asynchronously."""
        response = await self._http.post(f"/forms/{form_id}/unpublish")
        return Form.model_validate(response)

    async def duplicate(self, form_id: int) -> Form:
        """Duplicate a form asynchronously."""
        response = await self._http.post(f"/forms/{form_id}/duplicate")
        return Form.model_validate(response)
