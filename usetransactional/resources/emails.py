"""
Emails Resource

Email sending operations.
"""

from typing import Any, Dict, List, Optional, Union

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import EmailSendResult, EmailAttachment, EmailHeader


def _build_send_payload(
    from_email: str,
    to: Union[str, List[str]],
    subject: Optional[str] = None,
    html_body: Optional[str] = None,
    text_body: Optional[str] = None,
    template_id: Optional[int] = None,
    template_alias: Optional[str] = None,
    template_model: Optional[Dict[str, Any]] = None,
    cc: Optional[Union[str, List[str]]] = None,
    bcc: Optional[Union[str, List[str]]] = None,
    reply_to: Optional[str] = None,
    tag: Optional[str] = None,
    track_opens: Optional[bool] = None,
    track_links: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    attachments: Optional[List[EmailAttachment]] = None,
    headers: Optional[List[EmailHeader]] = None,
    message_stream: Optional[str] = None,
) -> Dict[str, Any]:
    """Build request payload for sending email."""
    payload: Dict[str, Any] = {
        "From": from_email,
        "To": to if isinstance(to, str) else ",".join(to),
    }

    if subject:
        payload["Subject"] = subject
    if html_body:
        payload["HtmlBody"] = html_body
    if text_body:
        payload["TextBody"] = text_body
    if template_id:
        payload["TemplateId"] = template_id
    if template_alias:
        payload["TemplateAlias"] = template_alias
    if template_model:
        payload["TemplateModel"] = template_model
    if cc:
        payload["Cc"] = cc if isinstance(cc, str) else ",".join(cc)
    if bcc:
        payload["Bcc"] = bcc if isinstance(bcc, str) else ",".join(bcc)
    if reply_to:
        payload["ReplyTo"] = reply_to
    if tag:
        payload["Tag"] = tag
    if track_opens is not None:
        payload["TrackOpens"] = track_opens
    if track_links:
        payload["TrackLinks"] = track_links
    if metadata:
        payload["Metadata"] = metadata
    if attachments:
        payload["Attachments"] = [
            {
                "Name": a.name,
                "Content": a.content,
                "ContentType": a.content_type,
                **({"ContentId": a.content_id} if a.content_id else {}),
            }
            for a in attachments
        ]
    if headers:
        payload["Headers"] = [{"Name": h.name, "Value": h.value} for h in headers]
    if message_stream:
        payload["MessageStream"] = message_stream

    return payload


class Emails(BaseResource):
    """Email sending operations."""

    def send(
        self,
        from_email: str,
        to: Union[str, List[str]],
        subject: Optional[str] = None,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        tag: Optional[str] = None,
        track_opens: Optional[bool] = None,
        track_links: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        attachments: Optional[List[EmailAttachment]] = None,
        headers: Optional[List[EmailHeader]] = None,
        message_stream: Optional[str] = None,
    ) -> EmailSendResult:
        """
        Send a single email.

        Args:
            from_email: Sender email address
            to: Recipient email address(es)
            subject: Email subject
            html_body: HTML content
            text_body: Plain text content
            cc: CC recipients
            bcc: BCC recipients
            reply_to: Reply-to address
            tag: Tag for categorization
            track_opens: Enable open tracking
            track_links: Link tracking mode
            metadata: Custom metadata
            attachments: File attachments
            headers: Custom headers
            message_stream: Message stream ID

        Returns:
            EmailSendResult with message ID and status
        """
        payload = _build_send_payload(
            from_email=from_email,
            to=to,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            tag=tag,
            track_opens=track_opens,
            track_links=track_links,
            metadata=metadata,
            attachments=attachments,
            headers=headers,
            message_stream=message_stream,
        )

        response = self._http.post("/email", json=payload)
        return EmailSendResult.model_validate(response)

    def send_with_template(
        self,
        from_email: str,
        to: Union[str, List[str]],
        template_id: Optional[int] = None,
        template_alias: Optional[str] = None,
        template_model: Optional[Dict[str, Any]] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        tag: Optional[str] = None,
        track_opens: Optional[bool] = None,
        track_links: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        attachments: Optional[List[EmailAttachment]] = None,
        headers: Optional[List[EmailHeader]] = None,
        message_stream: Optional[str] = None,
    ) -> EmailSendResult:
        """
        Send an email using a template.

        Args:
            from_email: Sender email address
            to: Recipient email address(es)
            template_id: Template ID
            template_alias: Template alias
            template_model: Template variables
            cc: CC recipients
            bcc: BCC recipients
            reply_to: Reply-to address
            tag: Tag for categorization
            track_opens: Enable open tracking
            track_links: Link tracking mode
            metadata: Custom metadata
            attachments: File attachments
            headers: Custom headers
            message_stream: Message stream ID

        Returns:
            EmailSendResult with message ID and status
        """
        payload = _build_send_payload(
            from_email=from_email,
            to=to,
            template_id=template_id,
            template_alias=template_alias,
            template_model=template_model,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            tag=tag,
            track_opens=track_opens,
            track_links=track_links,
            metadata=metadata,
            attachments=attachments,
            headers=headers,
            message_stream=message_stream,
        )

        response = self._http.post("/email/withTemplate", json=payload)
        return EmailSendResult.model_validate(response)

    def send_batch(
        self,
        messages: List[Dict[str, Any]],
    ) -> List[EmailSendResult]:
        """
        Send multiple emails in a batch.

        Args:
            messages: List of email message dicts with keys:
                - from_email: Sender email
                - to: Recipient(s)
                - subject: Subject
                - html_body: HTML content
                - text_body: Text content
                - And other optional fields

        Returns:
            List of EmailSendResult for each message
        """
        payloads = []
        for msg in messages:
            payload = _build_send_payload(
                from_email=msg.get("from_email", msg.get("from", "")),
                to=msg.get("to", ""),
                subject=msg.get("subject"),
                html_body=msg.get("html_body"),
                text_body=msg.get("text_body"),
                cc=msg.get("cc"),
                bcc=msg.get("bcc"),
                reply_to=msg.get("reply_to"),
                tag=msg.get("tag"),
                track_opens=msg.get("track_opens"),
                track_links=msg.get("track_links"),
                metadata=msg.get("metadata"),
                attachments=msg.get("attachments"),
                headers=msg.get("headers"),
                message_stream=msg.get("message_stream"),
            )
            payloads.append(payload)

        response = self._http.post("/email/batch", json=payloads)
        return [EmailSendResult.model_validate(r) for r in response]


class AsyncEmails(AsyncBaseResource):
    """Asynchronous email sending operations."""

    async def send(
        self,
        from_email: str,
        to: Union[str, List[str]],
        subject: Optional[str] = None,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        tag: Optional[str] = None,
        track_opens: Optional[bool] = None,
        track_links: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        attachments: Optional[List[EmailAttachment]] = None,
        headers: Optional[List[EmailHeader]] = None,
        message_stream: Optional[str] = None,
    ) -> EmailSendResult:
        """Send a single email asynchronously."""
        payload = _build_send_payload(
            from_email=from_email,
            to=to,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            tag=tag,
            track_opens=track_opens,
            track_links=track_links,
            metadata=metadata,
            attachments=attachments,
            headers=headers,
            message_stream=message_stream,
        )

        response = await self._http.post("/email", json=payload)
        return EmailSendResult.model_validate(response)

    async def send_with_template(
        self,
        from_email: str,
        to: Union[str, List[str]],
        template_id: Optional[int] = None,
        template_alias: Optional[str] = None,
        template_model: Optional[Dict[str, Any]] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        reply_to: Optional[str] = None,
        tag: Optional[str] = None,
        track_opens: Optional[bool] = None,
        track_links: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
        attachments: Optional[List[EmailAttachment]] = None,
        headers: Optional[List[EmailHeader]] = None,
        message_stream: Optional[str] = None,
    ) -> EmailSendResult:
        """Send an email using a template asynchronously."""
        payload = _build_send_payload(
            from_email=from_email,
            to=to,
            template_id=template_id,
            template_alias=template_alias,
            template_model=template_model,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            tag=tag,
            track_opens=track_opens,
            track_links=track_links,
            metadata=metadata,
            attachments=attachments,
            headers=headers,
            message_stream=message_stream,
        )

        response = await self._http.post("/email/withTemplate", json=payload)
        return EmailSendResult.model_validate(response)

    async def send_batch(
        self,
        messages: List[Dict[str, Any]],
    ) -> List[EmailSendResult]:
        """Send multiple emails in a batch asynchronously."""
        payloads = []
        for msg in messages:
            payload = _build_send_payload(
                from_email=msg.get("from_email", msg.get("from", "")),
                to=msg.get("to", ""),
                subject=msg.get("subject"),
                html_body=msg.get("html_body"),
                text_body=msg.get("text_body"),
                cc=msg.get("cc"),
                bcc=msg.get("bcc"),
                reply_to=msg.get("reply_to"),
                tag=msg.get("tag"),
                track_opens=msg.get("track_opens"),
                track_links=msg.get("track_links"),
                metadata=msg.get("metadata"),
                attachments=msg.get("attachments"),
                headers=msg.get("headers"),
                message_stream=msg.get("message_stream"),
            )
            payloads.append(payload)

        response = await self._http.post("/email/batch", json=payloads)
        return [EmailSendResult.model_validate(r) for r in response]
