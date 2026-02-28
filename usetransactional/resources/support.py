"""
Support Resource

Support/Chat operations.
"""

from typing import Any, Dict, List, Optional

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.types import (
    Conversation,
    ConversationList,
    ConversationMessage,
    ConversationListItem,
    Visitor,
    VisitorList,
    VisitorSession,
    VisitorEvent,
    Company,
    CompanyList,
    CompanyNote,
    CompanyStats,
    Inbox,
    InboxMember,
    InboxStats,
    CannedResponse,
    SupportWebhook,
    WebhookLogEntry,
    AnalyticsOverview,
    TeamPerformance,
)


class Conversations(BaseResource):
    """Conversations operations."""

    def list(
        self,
        status: Optional[str] = None,
        inbox_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
        visitor_id: Optional[str] = None,
        tag: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> ConversationList:
        """
        List conversations.

        Args:
            status: Filter by status (OPEN, PENDING, RESOLVED, CLOSED)
            inbox_id: Filter by inbox ID
            assignee_id: Filter by assignee ID
            visitor_id: Filter by visitor ID
            tag: Filter by tag
            page: Page number
            limit: Items per page

        Returns:
            ConversationList with conversations and pagination
        """
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if status:
            params["status"] = status
        if inbox_id:
            params["inboxId"] = inbox_id
        if assignee_id:
            params["assigneeId"] = assignee_id
        if visitor_id:
            params["visitorId"] = visitor_id
        if tag:
            params["tag"] = tag

        response = self._http.get("/support/conversations", params=params)
        return ConversationList.model_validate(response)

    def get(self, conversation_id: str) -> Conversation:
        """
        Get a conversation by ID.

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation details
        """
        response = self._http.get(f"/support/conversations/{conversation_id}")
        return Conversation.model_validate(response)

    def reply(
        self,
        conversation_id: str,
        message: str,
        message_type: str = "reply",
        attachments: Optional[List[str]] = None,
    ) -> ConversationMessage:
        """
        Reply to a conversation.

        Args:
            conversation_id: Conversation ID
            message: Message content
            message_type: Message type (reply, note)
            attachments: Attachment IDs

        Returns:
            Sent message
        """
        payload: Dict[str, Any] = {
            "message": message,
            "type": message_type,
        }
        if attachments:
            payload["attachments"] = attachments

        response = self._http.post(f"/support/conversations/{conversation_id}/reply", json=payload)
        return ConversationMessage.model_validate(response)

    def assign(self, conversation_id: str, assignee_id: str) -> Conversation:
        """
        Assign a conversation to an agent.

        Args:
            conversation_id: Conversation ID
            assignee_id: Agent ID

        Returns:
            Updated conversation
        """
        payload = {"assigneeId": assignee_id}
        response = self._http.post(f"/support/conversations/{conversation_id}/assign", json=payload)
        return Conversation.model_validate(response)

    def update(
        self,
        conversation_id: str,
        status: Optional[str] = None,
        priority: Optional[int] = None,
    ) -> Conversation:
        """
        Update conversation status.

        Args:
            conversation_id: Conversation ID
            status: New status
            priority: Priority (1-5)

        Returns:
            Updated conversation
        """
        payload: Dict[str, Any] = {}
        if status:
            payload["status"] = status
        if priority is not None:
            payload["priority"] = priority

        response = self._http.put(f"/support/conversations/{conversation_id}", json=payload)
        return Conversation.model_validate(response)

    def close(self, conversation_id: str) -> Conversation:
        """
        Close a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            Closed conversation
        """
        return self.update(conversation_id, status="CLOSED")

    def reopen(self, conversation_id: str) -> Conversation:
        """
        Reopen a conversation.

        Args:
            conversation_id: Conversation ID

        Returns:
            Reopened conversation
        """
        return self.update(conversation_id, status="OPEN")

    def snooze(self, conversation_id: str, until: str) -> Conversation:
        """
        Snooze a conversation.

        Args:
            conversation_id: Conversation ID
            until: Snooze until (ISO 8601)

        Returns:
            Snoozed conversation
        """
        payload = {"until": until}
        response = self._http.post(f"/support/conversations/{conversation_id}/snooze", json=payload)
        return Conversation.model_validate(response)

    def add_tags(self, conversation_id: str, tags: List[str]) -> Conversation:
        """
        Add tags to a conversation.

        Args:
            conversation_id: Conversation ID
            tags: Tag names

        Returns:
            Updated conversation
        """
        payload = {"tags": tags}
        response = self._http.post(f"/support/conversations/{conversation_id}/tags", json=payload)
        return Conversation.model_validate(response)

    def remove_tag(self, conversation_id: str, tag_id: str) -> None:
        """
        Remove a tag from a conversation.

        Args:
            conversation_id: Conversation ID
            tag_id: Tag ID
        """
        self._http.delete(f"/support/conversations/{conversation_id}/tags/{tag_id}")


class Visitors(BaseResource):
    """Visitors operations."""

    def list(
        self,
        search: Optional[str] = None,
        identified: Optional[bool] = None,
        company_id: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> VisitorList:
        """
        List visitors.

        Args:
            search: Search by name or email
            identified: Filter by identification status
            company_id: Filter by company ID
            page: Page number
            limit: Items per page

        Returns:
            VisitorList with visitors and pagination
        """
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if search:
            params["search"] = search
        if identified is not None:
            params["identified"] = identified
        if company_id:
            params["companyId"] = company_id

        response = self._http.get("/support/visitors", params=params)
        return VisitorList.model_validate(response)

    def get(self, visitor_id: str) -> Visitor:
        """
        Get a visitor by ID.

        Args:
            visitor_id: Visitor ID

        Returns:
            Visitor details
        """
        response = self._http.get(f"/support/visitors/{visitor_id}")
        return Visitor.model_validate(response)

    def update(
        self,
        visitor_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        avatar: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Visitor:
        """
        Update a visitor.

        Args:
            visitor_id: Visitor ID
            name: Visitor name
            email: Visitor email
            phone: Visitor phone
            avatar: Avatar URL
            attributes: Custom attributes

        Returns:
            Updated visitor
        """
        payload: Dict[str, Any] = {}
        if name:
            payload["name"] = name
        if email:
            payload["email"] = email
        if phone:
            payload["phone"] = phone
        if avatar:
            payload["avatar"] = avatar
        if attributes:
            payload["attributes"] = attributes

        response = self._http.put(f"/support/visitors/{visitor_id}", json=payload)
        return Visitor.model_validate(response)

    def delete(self, visitor_id: str) -> None:
        """
        Delete a visitor.

        Args:
            visitor_id: Visitor ID
        """
        self._http.delete(f"/support/visitors/{visitor_id}")

    def get_sessions(self, visitor_id: str) -> List[VisitorSession]:
        """
        Get visitor sessions.

        Args:
            visitor_id: Visitor ID

        Returns:
            Sessions list
        """
        response = self._http.get(f"/support/visitors/{visitor_id}/sessions")
        return [VisitorSession.model_validate(s) for s in response]

    def get_events(self, visitor_id: str) -> List[VisitorEvent]:
        """
        Get visitor events.

        Args:
            visitor_id: Visitor ID

        Returns:
            Events list
        """
        response = self._http.get(f"/support/visitors/{visitor_id}/events")
        return [VisitorEvent.model_validate(e) for e in response]

    def get_conversations(self, visitor_id: str) -> List[ConversationListItem]:
        """
        Get visitor conversations.

        Args:
            visitor_id: Visitor ID

        Returns:
            Conversations list
        """
        response = self._http.get(f"/support/visitors/{visitor_id}/conversations")
        return [ConversationListItem.model_validate(c) for c in response]

    def track_event(
        self,
        visitor_id: str,
        name: str,
        properties: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> None:
        """
        Track an event for a visitor.

        Args:
            visitor_id: Visitor ID
            name: Event name
            properties: Event properties
            timestamp: Event timestamp (ISO 8601)
        """
        payload: Dict[str, Any] = {"name": name}
        if properties:
            payload["properties"] = properties
        if timestamp:
            payload["timestamp"] = timestamp

        self._http.post(f"/support/visitors/{visitor_id}/events", json=payload)

    def associate_company(self, visitor_id: str, company_id: str) -> Visitor:
        """
        Associate visitor with a company.

        Args:
            visitor_id: Visitor ID
            company_id: Company ID

        Returns:
            Updated visitor
        """
        payload = {"companyId": company_id}
        response = self._http.put(f"/support/visitors/{visitor_id}/company", json=payload)
        return Visitor.model_validate(response)

    def export(self, visitor_id: str) -> Dict[str, Any]:
        """
        Export visitor data.

        Args:
            visitor_id: Visitor ID

        Returns:
            Visitor data export
        """
        return self._http.get(f"/support/visitors/{visitor_id}/export")

    def anonymize(self, visitor_id: str) -> None:
        """
        Anonymize visitor data (GDPR).

        Args:
            visitor_id: Visitor ID
        """
        self._http.post(f"/support/visitors/{visitor_id}/anonymize")


class Companies(BaseResource):
    """Companies operations."""

    def list(
        self,
        search: Optional[str] = None,
        industry: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> CompanyList:
        """
        List companies.

        Args:
            search: Search by name
            industry: Filter by industry
            page: Page number
            limit: Items per page

        Returns:
            CompanyList with companies and pagination
        """
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if search:
            params["search"] = search
        if industry:
            params["industry"] = industry

        response = self._http.get("/support/companies", params=params)
        return CompanyList.model_validate(response)

    def get(self, company_id: str) -> Company:
        """
        Get a company by ID.

        Args:
            company_id: Company ID

        Returns:
            Company details
        """
        response = self._http.get(f"/support/companies/{company_id}")
        return Company.model_validate(response)

    def create(
        self,
        name: str,
        company_id: Optional[str] = None,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Company:
        """
        Create a company.

        Args:
            name: Company name
            company_id: External company ID
            website: Website
            industry: Industry
            size: Company size
            attributes: Custom attributes

        Returns:
            Created company
        """
        payload: Dict[str, Any] = {"name": name}
        if company_id:
            payload["id"] = company_id
        if website:
            payload["website"] = website
        if industry:
            payload["industry"] = industry
        if size:
            payload["size"] = size
        if attributes:
            payload["attributes"] = attributes

        response = self._http.post("/support/companies", json=payload)
        return Company.model_validate(response)

    def update(
        self,
        company_id: str,
        name: Optional[str] = None,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Company:
        """
        Update a company.

        Args:
            company_id: Company ID
            name: Company name
            website: Website
            industry: Industry
            size: Company size
            attributes: Custom attributes

        Returns:
            Updated company
        """
        payload: Dict[str, Any] = {}
        if name:
            payload["name"] = name
        if website:
            payload["website"] = website
        if industry:
            payload["industry"] = industry
        if size:
            payload["size"] = size
        if attributes:
            payload["attributes"] = attributes

        response = self._http.put(f"/support/companies/{company_id}", json=payload)
        return Company.model_validate(response)

    def delete(self, company_id: str) -> None:
        """
        Delete a company.

        Args:
            company_id: Company ID
        """
        self._http.delete(f"/support/companies/{company_id}")

    def get_users(self, company_id: str) -> List[Visitor]:
        """
        Get company visitors.

        Args:
            company_id: Company ID

        Returns:
            Visitors list
        """
        response = self._http.get(f"/support/companies/{company_id}/users")
        return [Visitor.model_validate(v) for v in response]

    def get_conversations(self, company_id: str) -> List[ConversationListItem]:
        """
        Get company conversations.

        Args:
            company_id: Company ID

        Returns:
            Conversations list
        """
        response = self._http.get(f"/support/companies/{company_id}/conversations")
        return [ConversationListItem.model_validate(c) for c in response]

    def get_stats(self, company_id: str) -> CompanyStats:
        """
        Get company statistics.

        Args:
            company_id: Company ID

        Returns:
            Company stats
        """
        response = self._http.get(f"/support/companies/{company_id}/stats")
        return CompanyStats.model_validate(response)

    def add_note(self, company_id: str, content: str) -> CompanyNote:
        """
        Add a note to a company.

        Args:
            company_id: Company ID
            content: Note content

        Returns:
            Created note
        """
        payload = {"content": content}
        response = self._http.post(f"/support/companies/{company_id}/notes", json=payload)
        return CompanyNote.model_validate(response)


class Inboxes(BaseResource):
    """Inboxes operations."""

    def list(self) -> List[Inbox]:
        """
        List inboxes.

        Returns:
            Inboxes list
        """
        response = self._http.get("/support/inboxes")
        return [Inbox.model_validate(i) for i in response]

    def get(self, inbox_id: str) -> Inbox:
        """
        Get an inbox by ID.

        Args:
            inbox_id: Inbox ID

        Returns:
            Inbox details
        """
        response = self._http.get(f"/support/inboxes/{inbox_id}")
        return Inbox.model_validate(response)

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Inbox:
        """
        Create an inbox.

        Args:
            name: Inbox name
            description: Inbox description
            email: Inbox email

        Returns:
            Created inbox
        """
        payload: Dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        if email:
            payload["email"] = email

        response = self._http.post("/support/inboxes", json=payload)
        return Inbox.model_validate(response)

    def update(
        self,
        inbox_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Inbox:
        """
        Update an inbox.

        Args:
            inbox_id: Inbox ID
            name: Inbox name
            description: Inbox description
            email: Inbox email

        Returns:
            Updated inbox
        """
        payload: Dict[str, Any] = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if email:
            payload["email"] = email

        response = self._http.put(f"/support/inboxes/{inbox_id}", json=payload)
        return Inbox.model_validate(response)

    def delete(self, inbox_id: str) -> None:
        """
        Delete an inbox.

        Args:
            inbox_id: Inbox ID
        """
        self._http.delete(f"/support/inboxes/{inbox_id}")

    def get_stats(self, inbox_id: str) -> InboxStats:
        """
        Get inbox statistics.

        Args:
            inbox_id: Inbox ID

        Returns:
            Inbox stats
        """
        response = self._http.get(f"/support/inboxes/{inbox_id}/stats")
        return InboxStats.model_validate(response)

    def list_members(self, inbox_id: str) -> List[InboxMember]:
        """
        List inbox members.

        Args:
            inbox_id: Inbox ID

        Returns:
            Members list
        """
        response = self._http.get(f"/support/inboxes/{inbox_id}/members")
        return [InboxMember.model_validate(m) for m in response]

    def add_member(self, inbox_id: str, user_id: str, role: str) -> InboxMember:
        """
        Add a member to an inbox.

        Args:
            inbox_id: Inbox ID
            user_id: User ID
            role: Role (ADMIN, AGENT, VIEWER)

        Returns:
            Added member
        """
        payload = {"userId": user_id, "role": role}
        response = self._http.post(f"/support/inboxes/{inbox_id}/members", json=payload)
        return InboxMember.model_validate(response)

    def remove_member(self, inbox_id: str, user_id: str) -> None:
        """
        Remove a member from an inbox.

        Args:
            inbox_id: Inbox ID
            user_id: User ID
        """
        self._http.delete(f"/support/inboxes/{inbox_id}/members/{user_id}")

    def update_availability(self, inbox_id: str, user_id: str, status: str) -> InboxMember:
        """
        Update member availability.

        Args:
            inbox_id: Inbox ID
            user_id: User ID
            status: Availability status (AVAILABLE, AWAY, BUSY, OFFLINE)

        Returns:
            Updated member
        """
        payload = {"status": status}
        response = self._http.put(f"/support/inboxes/{inbox_id}/members/{user_id}/availability", json=payload)
        return InboxMember.model_validate(response)


class CannedResponses(BaseResource):
    """Canned responses operations."""

    def list(
        self,
        search: Optional[str] = None,
        shared: Optional[bool] = None,
        page: int = 1,
        limit: int = 20,
    ) -> List[CannedResponse]:
        """
        List canned responses.

        Args:
            search: Search by title or shortcut
            shared: Filter by shared status
            page: Page number
            limit: Items per page

        Returns:
            Canned responses list
        """
        params: Dict[str, Any] = {
            "page": page,
            "limit": limit,
        }
        if search:
            params["search"] = search
        if shared is not None:
            params["shared"] = shared

        response = self._http.get("/support/canned-responses", params=params)
        return [CannedResponse.model_validate(r) for r in response]

    def get(self, response_id: str) -> CannedResponse:
        """
        Get a canned response by ID.

        Args:
            response_id: Response ID

        Returns:
            Canned response details
        """
        response = self._http.get(f"/support/canned-responses/{response_id}")
        return CannedResponse.model_validate(response)

    def create(
        self,
        title: str,
        shortcut: str,
        content: str,
        is_shared: bool = False,
    ) -> CannedResponse:
        """
        Create a canned response.

        Args:
            title: Response title
            shortcut: Shortcut (e.g., /hello)
            content: Response content
            is_shared: Is shared with team

        Returns:
            Created canned response
        """
        payload = {
            "title": title,
            "shortcut": shortcut,
            "content": content,
            "isShared": is_shared,
        }
        response = self._http.post("/support/canned-responses", json=payload)
        return CannedResponse.model_validate(response)

    def update(
        self,
        response_id: str,
        title: Optional[str] = None,
        shortcut: Optional[str] = None,
        content: Optional[str] = None,
        is_shared: Optional[bool] = None,
    ) -> CannedResponse:
        """
        Update a canned response.

        Args:
            response_id: Response ID
            title: Response title
            shortcut: Shortcut
            content: Response content
            is_shared: Is shared with team

        Returns:
            Updated canned response
        """
        payload: Dict[str, Any] = {}
        if title:
            payload["title"] = title
        if shortcut:
            payload["shortcut"] = shortcut
        if content:
            payload["content"] = content
        if is_shared is not None:
            payload["isShared"] = is_shared

        response = self._http.put(f"/support/canned-responses/{response_id}", json=payload)
        return CannedResponse.model_validate(response)

    def delete(self, response_id: str) -> None:
        """
        Delete a canned response.

        Args:
            response_id: Response ID
        """
        self._http.delete(f"/support/canned-responses/{response_id}")


class SupportWebhooks(BaseResource):
    """Support webhooks operations."""

    def list(self) -> List[SupportWebhook]:
        """
        List webhooks.

        Returns:
            Webhooks list
        """
        response = self._http.get("/support/webhooks")
        return [SupportWebhook.model_validate(w) for w in response]

    def create(
        self,
        url: str,
        events: List[str],
        secret: Optional[str] = None,
    ) -> SupportWebhook:
        """
        Create a webhook.

        Args:
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

        response = self._http.post("/support/webhooks", json=payload)
        return SupportWebhook.model_validate(response)

    def delete(self, webhook_id: str) -> None:
        """
        Delete a webhook.

        Args:
            webhook_id: Webhook ID
        """
        self._http.delete(f"/support/webhooks/{webhook_id}")

    def get_logs(self, webhook_id: str) -> List[WebhookLogEntry]:
        """
        Get webhook logs.

        Args:
            webhook_id: Webhook ID

        Returns:
            Webhook logs
        """
        response = self._http.get(f"/support/webhooks/{webhook_id}/logs")
        return [WebhookLogEntry.model_validate(l) for l in response]


class SupportAnalytics(BaseResource):
    """Support analytics operations."""

    def get_overview(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> AnalyticsOverview:
        """
        Get overview analytics.

        Args:
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            Analytics overview
        """
        params: Dict[str, Any] = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = self._http.get("/support/analytics/overview", params=params)
        return AnalyticsOverview.model_validate(response)

    def get_conversations(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get conversation analytics.

        Args:
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            Conversation analytics
        """
        params: Dict[str, Any] = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        return self._http.get("/support/analytics/conversations", params=params)

    def get_team(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[TeamPerformance]:
        """
        Get team performance.

        Args:
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            Team performance data
        """
        params: Dict[str, Any] = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = self._http.get("/support/analytics/team", params=params)
        return [TeamPerformance.model_validate(t) for t in response]

    def get_response_time(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get response time analytics.

        Args:
            start_date: Start date (ISO 8601)
            end_date: End date (ISO 8601)

        Returns:
            Response time data
        """
        params: Dict[str, Any] = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        return self._http.get("/support/analytics/response-time", params=params)


class Support(BaseResource):
    """Support operations."""

    def __init__(self, http: Any) -> None:
        super().__init__(http)
        self.conversations = Conversations(http)
        self.visitors = Visitors(http)
        self.companies = Companies(http)
        self.inboxes = Inboxes(http)
        self.canned_responses = CannedResponses(http)
        self.webhooks = SupportWebhooks(http)
        self.analytics = SupportAnalytics(http)


# Async versions would follow the same pattern as Forms
# For brevity, we'll add a placeholder comment
# In production, implement all async classes similar to AsyncForms


class AsyncSupport(AsyncBaseResource):
    """Asynchronous support operations (placeholder)."""

    def __init__(self, http: Any) -> None:
        super().__init__(http)
        # Async sub-resources would be initialized here
