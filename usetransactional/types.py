"""
Transactional SDK Types

Type definitions using Pydantic models.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


# ===========================================
# EMAIL TYPES
# ===========================================


class EmailSendResult(BaseModel):
    """Result of sending an email."""

    message_id: str = Field(alias="messageId")
    to: str
    submitted_at: Optional[datetime] = Field(None, alias="submittedAt")
    error_code: int = Field(alias="errorCode")
    message: str


class EmailBatchResult(BaseModel):
    """Result of sending batch emails."""

    results: List[EmailSendResult]


class EmailRecipient(BaseModel):
    """Email recipient with optional name."""

    email: str
    name: Optional[str] = None


class EmailAttachment(BaseModel):
    """Email attachment."""

    name: str
    content: str
    content_type: str = Field(alias="contentType")
    content_id: Optional[str] = Field(None, alias="contentId")


class EmailHeader(BaseModel):
    """Custom email header."""

    name: str
    value: str


class EmailMessage(BaseModel):
    """Full email message details."""

    message_id: str = Field(alias="messageId")
    status: str
    from_email: str = Field(alias="from")
    to: List[str]
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    subject: str
    tag: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    received_at: Optional[datetime] = Field(None, alias="receivedAt")


class EmailMessageList(BaseModel):
    """Paginated list of email messages."""

    total_count: int = Field(alias="totalCount")
    messages: List[EmailMessage]


# ===========================================
# TEMPLATE TYPES
# ===========================================


class TemplateType(str, Enum):
    """Template type."""

    STANDARD = "Standard"
    LAYOUT = "Layout"


class Template(BaseModel):
    """Email template."""

    template_id: int = Field(alias="templateId")
    name: str
    alias: Optional[str] = None
    subject: str
    html_body: Optional[str] = Field(None, alias="htmlBody")
    text_body: Optional[str] = Field(None, alias="textBody")
    template_type: TemplateType = Field(alias="templateType")
    layout_template: Optional[str] = Field(None, alias="layoutTemplate")
    active: bool
    associated_server_id: Optional[int] = Field(None, alias="associatedServerId")


class TemplateList(BaseModel):
    """Paginated list of templates."""

    total_count: int = Field(alias="totalCount")
    templates: List[Template]


# ===========================================
# SUPPRESSION TYPES
# ===========================================


class SuppressionReason(str, Enum):
    """Suppression reason."""

    HARD_BOUNCE = "HardBounce"
    SPAM_COMPLAINT = "SpamComplaint"
    MANUAL = "ManualSuppression"


class Suppression(BaseModel):
    """Email suppression entry."""

    email_address: str = Field(alias="emailAddress")
    suppression_reason: SuppressionReason = Field(alias="suppressionReason")
    created_at: datetime = Field(alias="createdAt")
    origin: Optional[str] = None


class SuppressionList(BaseModel):
    """Paginated list of suppressions."""

    total_count: int = Field(alias="totalCount")
    suppressions: List[Suppression]


class SuppressionCheckResult(BaseModel):
    """Result of checking if an email is suppressed."""

    suppressed: bool
    reason: Optional[SuppressionReason] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")


# ===========================================
# BOUNCE TYPES
# ===========================================


class BounceType(str, Enum):
    """Bounce type."""

    HARD_BOUNCE = "HardBounce"
    SOFT_BOUNCE = "SoftBounce"
    TRANSIENT = "Transient"
    UNKNOWN = "Unknown"


class Bounce(BaseModel):
    """Email bounce record."""

    id: int
    type: BounceType
    type_code: int = Field(alias="typeCode")
    name: str
    tag: Optional[str] = None
    message_id: str = Field(alias="messageId")
    server_id: int = Field(alias="serverId")
    description: str
    details: Optional[str] = None
    email: str
    from_email: str = Field(alias="from")
    bounced_at: datetime = Field(alias="bouncedAt")
    dump_available: bool = Field(alias="dumpAvailable")
    inactive: bool
    can_activate: bool = Field(alias="canActivate")
    subject: Optional[str] = None


class BounceList(BaseModel):
    """Paginated list of bounces."""

    total_count: int = Field(alias="totalCount")
    bounces: List[Bounce]


# ===========================================
# SMS TYPES
# ===========================================


class SmsMessageStatus(str, Enum):
    """SMS message status."""

    QUEUED = "QUEUED"
    SENDING = "SENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    UNDELIVERED = "UNDELIVERED"
    BLOCKED = "BLOCKED"
    SUPPRESSED = "SUPPRESSED"


class SmsMessageDirection(str, Enum):
    """SMS message direction."""

    OUTBOUND = "OUTBOUND"
    INBOUND = "INBOUND"


class SmsCountry(str, Enum):
    """SMS country code."""

    US = "US"
    CA = "CA"
    GB = "GB"
    IN = "IN"


class SmsSuppressionReason(str, Enum):
    """SMS suppression reason."""

    OPT_OUT = "OPT_OUT"
    MANUAL = "MANUAL"
    CARRIER_BLOCK = "CARRIER_BLOCK"
    INVALID_NUMBER = "INVALID_NUMBER"


class SmsWebhookEventType(str, Enum):
    """SMS webhook event type."""

    QUEUED = "sms.queued"
    SENT = "sms.sent"
    DELIVERED = "sms.delivered"
    FAILED = "sms.failed"
    UNDELIVERED = "sms.undelivered"
    INBOUND = "sms.inbound"
    OPT_OUT = "sms.opt_out"
    OPT_IN = "sms.opt_in"


class SmsSendResult(BaseModel):
    """Result of sending an SMS."""

    to: str
    submitted_at: Optional[datetime] = Field(None, alias="submittedAt")
    message_id: Optional[str] = Field(None, alias="messageId")
    error_code: int = Field(alias="errorCode")
    message: str


class SmsEvent(BaseModel):
    """SMS message event."""

    event_type: str = Field(alias="eventType")
    timestamp: datetime
    raw_payload: Optional[Any] = Field(None, alias="rawPayload")


class SmsMessage(BaseModel):
    """Full SMS message details."""

    message_id: str = Field(alias="messageId")
    provider_message_id: Optional[str] = Field(None, alias="providerMessageId")
    from_number: str = Field(alias="from")
    to: str
    body: str
    status: SmsMessageStatus
    direction: SmsMessageDirection
    segments: int
    country: SmsCountry
    tag: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    error_code: Optional[int] = Field(None, alias="errorCode")
    error_message: Optional[str] = Field(None, alias="errorMessage")
    queued_at: Optional[datetime] = Field(None, alias="queuedAt")
    sent_at: Optional[datetime] = Field(None, alias="sentAt")
    delivered_at: Optional[datetime] = Field(None, alias="deliveredAt")
    failed_at: Optional[datetime] = Field(None, alias="failedAt")
    events: Optional[List[SmsEvent]] = None


class SmsMessageListItem(BaseModel):
    """SMS message list item (summary)."""

    message_id: str = Field(alias="messageId")
    from_number: str = Field(alias="from")
    to: str
    status: SmsMessageStatus
    direction: SmsMessageDirection
    segments: int
    country: SmsCountry
    tag: Optional[str] = None
    queued_at: Optional[datetime] = Field(None, alias="queuedAt")
    sent_at: Optional[datetime] = Field(None, alias="sentAt")
    delivered_at: Optional[datetime] = Field(None, alias="deliveredAt")
    failed_at: Optional[datetime] = Field(None, alias="failedAt")


class SmsMessageList(BaseModel):
    """Paginated list of SMS messages."""

    total_count: int = Field(alias="totalCount")
    messages: List[SmsMessageListItem]


class InboundSmsMessage(BaseModel):
    """Inbound SMS message."""

    message_id: str = Field(alias="messageId")
    provider_message_id: Optional[str] = Field(None, alias="providerMessageId")
    from_number: str = Field(alias="from")
    to: str
    body: str
    received_at: datetime = Field(alias="receivedAt")


class InboundSmsMessageList(BaseModel):
    """Paginated list of inbound SMS messages."""

    total_count: int = Field(alias="totalCount")
    messages: List[InboundSmsMessage]


class SmsSuppression(BaseModel):
    """SMS suppression entry."""

    phone_number: str = Field(alias="phoneNumber")
    phone_number_hash: str = Field(alias="phoneNumberHash")
    reason: SmsSuppressionReason
    opted_out_at: datetime = Field(alias="optedOutAt")
    notes: Optional[str] = None


class SmsSuppressionList(BaseModel):
    """Paginated list of SMS suppressions."""

    total_count: int = Field(alias="totalCount")
    suppressions: List[SmsSuppression]


class SmsSuppressionCheckResult(BaseModel):
    """Result of checking if a phone number is suppressed."""

    suppressed: bool
    reason: Optional[SmsSuppressionReason] = None
    opted_out_at: Optional[datetime] = Field(None, alias="optedOutAt")


class SmsWebhook(BaseModel):
    """SMS webhook."""

    id: str
    url: str
    secret: Optional[str] = None
    events: List[SmsWebhookEventType]
    is_active: bool = Field(alias="isActive")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class SmsPoolTemplate(BaseModel):
    """SMS pool template."""

    id: int
    alias: str
    name: str
    body: str
    category: str
    use_cases: List[str] = Field(alias="useCases")
    variables: List[str]
    is_active: bool = Field(alias="isActive")


class SmsOrgTemplate(BaseModel):
    """SMS organization template reference."""

    id: int
    pool_template_id: int = Field(alias="poolTemplateId")
    custom_alias: Optional[str] = Field(None, alias="customAlias")
    pool_template: SmsPoolTemplate = Field(alias="poolTemplate")
    is_active: bool = Field(alias="isActive")
    created_at: datetime = Field(alias="createdAt")


class SmsTemplateList(BaseModel):
    """Paginated list of SMS templates."""

    total_count: int = Field(alias="totalCount")
    templates: List[SmsOrgTemplate]


# ===========================================
# STATS TYPES
# ===========================================


class StatsSummary(BaseModel):
    """Email statistics summary."""

    sent: int
    bounced: int
    spam_complaints: int = Field(alias="spamComplaints")
    unique_opens: int = Field(alias="uniqueOpens")
    unique_clicks: int = Field(alias="uniqueClicks")
    total_opens: int = Field(alias="totalOpens")
    total_clicks: int = Field(alias="totalClicks")


class DailyStats(BaseModel):
    """Daily statistics."""

    date: str
    sent: int
    bounced: int
    spam_complaints: int = Field(alias="spamComplaints")
    unique_opens: int = Field(alias="uniqueOpens")
    unique_clicks: int = Field(alias="uniqueClicks")
    total_opens: int = Field(alias="totalOpens")
    total_clicks: int = Field(alias="totalClicks")


class StatsOverview(BaseModel):
    """Statistics overview response."""

    days: List[DailyStats]


# ===========================================
# FORMS TYPES
# ===========================================


class FormStatus(str, Enum):
    """Form status."""

    DRAFT = "DRAFT"
    LIVE = "LIVE"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class FormAccessType(str, Enum):
    """Form access type."""

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    PASSWORD_PROTECTED = "PASSWORD_PROTECTED"


class FormFieldType(str, Enum):
    """Form field type."""

    SHORT_TEXT = "SHORT_TEXT"
    LONG_TEXT = "LONG_TEXT"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    NUMBER = "NUMBER"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    URL = "URL"
    SINGLE_SELECT = "SINGLE_SELECT"
    MULTI_SELECT = "MULTI_SELECT"
    DROPDOWN = "DROPDOWN"
    CHECKBOX = "CHECKBOX"
    RATING = "RATING"
    FILE_UPLOAD = "FILE_UPLOAD"
    SIGNATURE = "SIGNATURE"
    STATEMENT = "STATEMENT"
    HIDDEN = "HIDDEN"


class FormThemePreset(str, Enum):
    """Form theme preset."""

    MODERN = "MODERN"
    CLASSIC = "CLASSIC"
    BOLD = "BOLD"
    MINIMAL = "MINIMAL"
    CUSTOM = "CUSTOM"


class SubmissionStatus(str, Enum):
    """Submission status."""

    PARTIAL = "PARTIAL"
    COMPLETE = "COMPLETE"


class FormFieldSettings(BaseModel):
    """Form field settings."""

    min_length: Optional[int] = Field(None, alias="minLength")
    max_length: Optional[int] = Field(None, alias="maxLength")
    min_value: Optional[int] = Field(None, alias="min")
    max_value: Optional[int] = Field(None, alias="max")
    options: Optional[List[Dict[str, str]]] = None
    accepted_file_types: Optional[List[str]] = Field(None, alias="acceptedFileTypes")
    max_file_size: Optional[int] = Field(None, alias="maxFileSize")
    default_value: Optional[Union[str, int, bool]] = Field(None, alias="defaultValue")
    pattern: Optional[str] = None
    validation_message: Optional[str] = Field(None, alias="validationMessage")


class FormField(BaseModel):
    """Form field."""

    id: int
    type: FormFieldType
    label: str
    placeholder: Optional[str] = None
    help_text: Optional[str] = Field(None, alias="helpText")
    required: bool
    order: int
    settings: Optional[FormFieldSettings] = None


class FormThemeColors(BaseModel):
    """Form theme colors."""

    primary: Optional[str] = None
    background: Optional[str] = None
    text: Optional[str] = None
    border: Optional[str] = None
    error: Optional[str] = None
    success: Optional[str] = None


class FormTheme(BaseModel):
    """Form theme."""

    preset: FormThemePreset
    colors: Optional[FormThemeColors] = None
    font_family: Optional[str] = Field(None, alias="fontFamily")
    border_radius: Optional[int] = Field(None, alias="borderRadius")
    custom_css: Optional[str] = Field(None, alias="customCss")


class FormSettings(BaseModel):
    """Form settings."""

    access_type: FormAccessType = Field(alias="accessType")
    password: Optional[str] = None
    redirect_url: Optional[str] = Field(None, alias="redirectUrl")
    thank_you_message: Optional[str] = Field(None, alias="thankYouMessage")
    notifications_enabled: Optional[bool] = Field(None, alias="notificationsEnabled")
    notification_emails: Optional[List[str]] = Field(None, alias="notificationEmails")
    close_date: Optional[str] = Field(None, alias="closeDate")
    max_submissions: Optional[int] = Field(None, alias="maxSubmissions")
    allow_multiple_submissions: Optional[bool] = Field(None, alias="allowMultipleSubmissions")
    show_progress_bar: Optional[bool] = Field(None, alias="showProgressBar")


class FormAnalytics(BaseModel):
    """Form analytics."""

    views: int
    starts: Optional[int] = None
    submissions: int
    completion_rate: float = Field(alias="completionRate")
    avg_completion_time: Optional[int] = Field(None, alias="avgCompletionTime")


class Form(BaseModel):
    """Form."""

    id: int
    uuid: str
    title: str
    slug: str
    description: Optional[str] = None
    status: FormStatus
    settings: FormSettings
    theme: FormTheme
    fields: List[FormField]
    analytics: Optional[FormAnalytics] = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    published_at: Optional[datetime] = Field(None, alias="publishedAt")


class FormListItem(BaseModel):
    """Form list item (summary)."""

    id: int
    uuid: str
    title: str
    slug: str
    status: FormStatus
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    published_at: Optional[datetime] = Field(None, alias="publishedAt")


class FormList(BaseModel):
    """Paginated list of forms."""

    data: List[FormListItem]
    meta: Dict[str, Any]


class FormSubmission(BaseModel):
    """Form submission."""

    id: int
    uuid: str
    form_id: int = Field(alias="formId")
    session_id: str = Field(alias="sessionId")
    status: SubmissionStatus
    data: Dict[str, Any]
    ip_address: Optional[str] = Field(None, alias="ipAddress")
    user_agent: Optional[str] = Field(None, alias="userAgent")
    referrer: Optional[str] = None
    created_at: datetime = Field(alias="createdAt")
    completed_at: Optional[datetime] = Field(None, alias="completedAt")


class FormSubmissionList(BaseModel):
    """Paginated list of form submissions."""

    data: List[FormSubmission]
    meta: Dict[str, Any]


class FormAnalyticsSummary(BaseModel):
    """Form analytics summary."""

    views: int
    starts: int
    completions: int
    completion_rate: float = Field(alias="completionRate")


class FormAnalyticsDataPoint(BaseModel):
    """Form analytics data point."""

    date: str
    views: int
    starts: int
    completions: int


class FormAnalyticsResponse(BaseModel):
    """Form analytics response."""

    summary: FormAnalyticsSummary
    data: List[FormAnalyticsDataPoint]


class FormWebhook(BaseModel):
    """Form webhook."""

    id: str
    url: str
    secret: Optional[str] = None
    events: List[str]
    is_active: bool = Field(alias="isActive")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


# ===========================================
# SUPPORT TYPES
# ===========================================


class ConversationStatus(str, Enum):
    """Conversation status."""

    OPEN = "OPEN"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class MessageType(str, Enum):
    """Message type."""

    REPLY = "REPLY"
    NOTE = "NOTE"
    SYSTEM = "SYSTEM"


class MessageSenderType(str, Enum):
    """Message sender type."""

    VISITOR = "VISITOR"
    AGENT = "AGENT"
    BOT = "BOT"
    SYSTEM = "SYSTEM"


class VisitorIdentificationStatus(str, Enum):
    """Visitor identification status."""

    ANONYMOUS = "ANONYMOUS"
    IDENTIFIED = "IDENTIFIED"


class AgentAvailability(str, Enum):
    """Agent availability status."""

    AVAILABLE = "AVAILABLE"
    AWAY = "AWAY"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"


class InboxMemberRole(str, Enum):
    """Inbox member role."""

    ADMIN = "ADMIN"
    AGENT = "AGENT"
    VIEWER = "VIEWER"


class ConversationParticipant(BaseModel):
    """Conversation participant."""

    id: str
    type: MessageSenderType
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None


class MessageAttachment(BaseModel):
    """Message attachment."""

    id: str
    name: str
    url: str
    size: int
    mime_type: str = Field(alias="mimeType")


class ConversationMessage(BaseModel):
    """Conversation message."""

    id: str
    content: str
    type: MessageType
    sender: ConversationParticipant
    attachments: Optional[List[MessageAttachment]] = None
    created_at: datetime = Field(alias="createdAt")
    read_at: Optional[datetime] = Field(None, alias="readAt")


class ConversationTag(BaseModel):
    """Conversation tag."""

    id: str
    name: str
    color: Optional[str] = None


class Visitor(BaseModel):
    """Visitor."""

    id: str
    external_id: Optional[str] = Field(None, alias="externalId")
    status: VisitorIdentificationStatus
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    company_id: Optional[str] = Field(None, alias="companyId")
    attributes: Optional[Dict[str, Any]] = None
    last_seen_at: Optional[datetime] = Field(None, alias="lastSeenAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class VisitorListItem(BaseModel):
    """Visitor list item (summary)."""

    id: str
    external_id: Optional[str] = Field(None, alias="externalId")
    status: VisitorIdentificationStatus
    name: Optional[str] = None
    email: Optional[str] = None
    company_name: Optional[str] = Field(None, alias="companyName")
    last_seen_at: Optional[datetime] = Field(None, alias="lastSeenAt")
    created_at: datetime = Field(alias="createdAt")


class VisitorList(BaseModel):
    """Paginated list of visitors."""

    data: List[VisitorListItem]
    meta: Dict[str, Any]


class VisitorSession(BaseModel):
    """Visitor session."""

    id: str
    ip_address: Optional[str] = Field(None, alias="ipAddress")
    user_agent: Optional[str] = Field(None, alias="userAgent")
    referrer: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    started_at: datetime = Field(alias="startedAt")
    ended_at: Optional[datetime] = Field(None, alias="endedAt")
    page_views: Optional[int] = Field(None, alias="pageViews")


class VisitorEvent(BaseModel):
    """Visitor event."""

    id: str
    name: str
    properties: Optional[Dict[str, Any]] = None
    timestamp: datetime


class Conversation(BaseModel):
    """Conversation."""

    id: str
    subject: Optional[str] = None
    status: ConversationStatus
    inbox_id: str = Field(alias="inboxId")
    visitor: Visitor
    assignee: Optional[ConversationParticipant] = None
    messages: List[ConversationMessage]
    tags: List[ConversationTag]
    priority: Optional[int] = None
    snoozed_until: Optional[datetime] = Field(None, alias="snoozedUntil")
    first_response_time: Optional[int] = Field(None, alias="firstResponseTime")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resolved_at: Optional[datetime] = Field(None, alias="resolvedAt")
    closed_at: Optional[datetime] = Field(None, alias="closedAt")


class ConversationListItem(BaseModel):
    """Conversation list item (summary)."""

    id: str
    subject: Optional[str] = None
    status: ConversationStatus
    inbox_id: str = Field(alias="inboxId")
    visitor: Dict[str, Any]
    assignee: Optional[Dict[str, Any]] = None
    last_message: Optional[Dict[str, Any]] = Field(None, alias="lastMessage")
    tags: List[ConversationTag]
    unread_count: int = Field(alias="unreadCount")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class ConversationList(BaseModel):
    """Paginated list of conversations."""

    data: List[ConversationListItem]
    meta: Dict[str, Any]


class Company(BaseModel):
    """Company."""

    id: str
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    visitor_count: Optional[int] = Field(None, alias="visitorCount")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CompanyList(BaseModel):
    """Paginated list of companies."""

    data: List[Company]
    meta: Dict[str, Any]


class CompanyNote(BaseModel):
    """Company note."""

    id: str
    content: str
    author: Dict[str, Any]
    created_at: datetime = Field(alias="createdAt")


class CompanyStats(BaseModel):
    """Company statistics."""

    total_conversations: int = Field(alias="totalConversations")
    open_conversations: int = Field(alias="openConversations")
    total_visitors: int = Field(alias="totalVisitors")
    avg_response_time: Optional[int] = Field(None, alias="avgResponseTime")


class Inbox(BaseModel):
    """Inbox."""

    id: str
    name: str
    description: Optional[str] = None
    email: Optional[str] = None
    is_default: bool = Field(alias="isDefault")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class InboxMember(BaseModel):
    """Inbox member."""

    user_id: str = Field(alias="userId")
    name: str
    email: str
    avatar: Optional[str] = None
    role: InboxMemberRole
    availability: AgentAvailability
    joined_at: datetime = Field(alias="joinedAt")


class InboxStats(BaseModel):
    """Inbox statistics."""

    total_conversations: int = Field(alias="totalConversations")
    open_conversations: int = Field(alias="openConversations")
    pending_conversations: int = Field(alias="pendingConversations")
    avg_response_time: Optional[int] = Field(None, alias="avgResponseTime")
    avg_resolution_time: Optional[int] = Field(None, alias="avgResolutionTime")


class CannedResponse(BaseModel):
    """Canned response."""

    id: str
    title: str
    shortcut: str
    content: str
    is_shared: bool = Field(alias="isShared")
    created_by: Dict[str, Any] = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class SupportWebhook(BaseModel):
    """Support webhook."""

    id: str
    url: str
    secret: Optional[str] = None
    events: List[str]
    is_active: bool = Field(alias="isActive")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class WebhookLogEntry(BaseModel):
    """Webhook log entry."""

    id: str
    event: str
    status: int
    response_time: int = Field(alias="responseTime")
    success: bool
    error: Optional[str] = None
    timestamp: datetime


class AnalyticsOverview(BaseModel):
    """Support analytics overview."""

    total_conversations: int = Field(alias="totalConversations")
    new_conversations: int = Field(alias="newConversations")
    resolved_conversations: int = Field(alias="resolvedConversations")
    avg_response_time: int = Field(alias="avgResponseTime")
    avg_resolution_time: int = Field(alias="avgResolutionTime")
    csat: Optional[float] = None


class TeamPerformance(BaseModel):
    """Team performance."""

    agent_id: str = Field(alias="agentId")
    agent_name: str = Field(alias="agentName")
    conversations_handled: int = Field(alias="conversationsHandled")
    messages_sent: int = Field(alias="messagesSent")
    avg_response_time: int = Field(alias="avgResponseTime")
    csat: Optional[float] = None
