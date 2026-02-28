"""
Templates Resource

Template management operations.
"""

from typing import Any, Dict, List, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import Template, TemplateList


class Templates(BaseResource):
    """Template management operations."""

    def list(
        self,
        count: int = 100,
        offset: int = 0,
        template_type: Optional[str] = None,
        layout_template: Optional[str] = None,
    ) -> TemplateList:
        """
        List templates.

        Args:
            count: Number of templates to return (max 500)
            offset: Pagination offset
            template_type: Filter by type ("Standard" or "Layout")
            layout_template: Filter by layout template alias

        Returns:
            TemplateList with templates and total count
        """
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if template_type:
            params["templateType"] = template_type
        if layout_template:
            params["layoutTemplate"] = layout_template

        response = self._http.get("/templates", params=params)
        return TemplateList.model_validate(response)

    def get(self, template_id: int) -> Template:
        """
        Get a template by ID.

        Args:
            template_id: Template ID

        Returns:
            Template details
        """
        response = self._http.get(f"/templates/{template_id}")
        return Template.model_validate(response)

    def get_by_alias(self, alias: str) -> Template:
        """
        Get a template by alias.

        Args:
            alias: Template alias

        Returns:
            Template details
        """
        response = self._http.get(f"/templates/alias/{alias}")
        return Template.model_validate(response)

    def create(
        self,
        name: str,
        subject: str,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        alias: Optional[str] = None,
        template_type: str = "Standard",
        layout_template: Optional[str] = None,
    ) -> Template:
        """
        Create a new template.

        Args:
            name: Template name
            subject: Email subject
            html_body: HTML content
            text_body: Plain text content
            alias: Template alias
            template_type: "Standard" or "Layout"
            layout_template: Layout template alias (for Standard templates)

        Returns:
            Created template
        """
        payload: Dict[str, Any] = {
            "Name": name,
            "Subject": subject,
            "TemplateType": template_type,
        }
        if html_body:
            payload["HtmlBody"] = html_body
        if text_body:
            payload["TextBody"] = text_body
        if alias:
            payload["Alias"] = alias
        if layout_template:
            payload["LayoutTemplate"] = layout_template

        response = self._http.post("/templates", json=payload)
        return Template.model_validate(response)

    def update(
        self,
        template_id: int,
        name: Optional[str] = None,
        subject: Optional[str] = None,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        alias: Optional[str] = None,
        layout_template: Optional[str] = None,
    ) -> Template:
        """
        Update an existing template.

        Args:
            template_id: Template ID
            name: Template name
            subject: Email subject
            html_body: HTML content
            text_body: Plain text content
            alias: Template alias
            layout_template: Layout template alias

        Returns:
            Updated template
        """
        payload: Dict[str, Any] = {}
        if name:
            payload["Name"] = name
        if subject:
            payload["Subject"] = subject
        if html_body is not None:
            payload["HtmlBody"] = html_body
        if text_body is not None:
            payload["TextBody"] = text_body
        if alias is not None:
            payload["Alias"] = alias
        if layout_template is not None:
            payload["LayoutTemplate"] = layout_template

        response = self._http.put(f"/templates/{template_id}", json=payload)
        return Template.model_validate(response)

    def delete(self, template_id: int) -> None:
        """
        Delete a template.

        Args:
            template_id: Template ID
        """
        self._http.delete(f"/templates/{template_id}")


class AsyncTemplates(AsyncBaseResource):
    """Asynchronous template management operations."""

    async def list(
        self,
        count: int = 100,
        offset: int = 0,
        template_type: Optional[str] = None,
        layout_template: Optional[str] = None,
    ) -> TemplateList:
        """List templates asynchronously."""
        params: Dict[str, Any] = {
            "count": count,
            "offset": offset,
        }
        if template_type:
            params["templateType"] = template_type
        if layout_template:
            params["layoutTemplate"] = layout_template

        response = await self._http.get("/templates", params=params)
        return TemplateList.model_validate(response)

    async def get(self, template_id: int) -> Template:
        """Get a template by ID asynchronously."""
        response = await self._http.get(f"/templates/{template_id}")
        return Template.model_validate(response)

    async def get_by_alias(self, alias: str) -> Template:
        """Get a template by alias asynchronously."""
        response = await self._http.get(f"/templates/alias/{alias}")
        return Template.model_validate(response)

    async def create(
        self,
        name: str,
        subject: str,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        alias: Optional[str] = None,
        template_type: str = "Standard",
        layout_template: Optional[str] = None,
    ) -> Template:
        """Create a new template asynchronously."""
        payload: Dict[str, Any] = {
            "Name": name,
            "Subject": subject,
            "TemplateType": template_type,
        }
        if html_body:
            payload["HtmlBody"] = html_body
        if text_body:
            payload["TextBody"] = text_body
        if alias:
            payload["Alias"] = alias
        if layout_template:
            payload["LayoutTemplate"] = layout_template

        response = await self._http.post("/templates", json=payload)
        return Template.model_validate(response)

    async def update(
        self,
        template_id: int,
        name: Optional[str] = None,
        subject: Optional[str] = None,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        alias: Optional[str] = None,
        layout_template: Optional[str] = None,
    ) -> Template:
        """Update an existing template asynchronously."""
        payload: Dict[str, Any] = {}
        if name:
            payload["Name"] = name
        if subject:
            payload["Subject"] = subject
        if html_body is not None:
            payload["HtmlBody"] = html_body
        if text_body is not None:
            payload["TextBody"] = text_body
        if alias is not None:
            payload["Alias"] = alias
        if layout_template is not None:
            payload["LayoutTemplate"] = layout_template

        response = await self._http.put(f"/templates/{template_id}", json=payload)
        return Template.model_validate(response)

    async def delete(self, template_id: int) -> None:
        """Delete a template asynchronously."""
        await self._http.delete(f"/templates/{template_id}")
