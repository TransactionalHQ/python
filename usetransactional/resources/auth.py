"""
Auth Resources

Resources for managing authentication, users, applications, sessions, MFA, SSO, and organizations.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


# ===========================================
# TYPES / MODELS
# ===========================================

class AuthUserProfile(BaseModel):
    """User profile information."""
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    display_name: Optional[str] = Field(None, alias="displayName")
    picture: Optional[str] = None
    locale: Optional[str] = None
    timezone: Optional[str] = None


class AuthUser(BaseModel):
    """Auth user model."""
    id: str
    external_id: Optional[str] = Field(None, alias="externalId")
    email: str
    email_verified: bool = Field(alias="emailVerified")
    phone: Optional[str] = None
    phone_verified: bool = Field(False, alias="phoneVerified")
    status: str
    profile: AuthUserProfile
    metadata: Optional[Dict[str, Any]] = None
    app_metadata: Optional[Dict[str, Any]] = Field(None, alias="appMetadata")
    login_count: int = Field(0, alias="loginCount")
    last_login_at: Optional[str] = Field(None, alias="lastLoginAt")
    last_login_ip: Optional[str] = Field(None, alias="lastLoginIp")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class AuthUserList(BaseModel):
    """List users response."""
    total_count: int = Field(alias="totalCount")
    users: List[AuthUser]


class AuthApplication(BaseModel):
    """Auth application model."""
    id: str
    client_id: str = Field(alias="clientId")
    client_secret: Optional[str] = Field(None, alias="clientSecret")
    name: str
    description: Optional[str] = None
    type: str
    logo_url: Optional[str] = Field(None, alias="logoUrl")
    redirect_uris: List[str] = Field(default_factory=list, alias="redirectUris")
    allowed_origins: List[str] = Field(default_factory=list, alias="allowedOrigins")
    logout_uris: List[str] = Field(default_factory=list, alias="logoutUris")
    grant_types: List[str] = Field(default_factory=list, alias="grantTypes")
    response_types: List[str] = Field(default_factory=list, alias="responseTypes")
    is_active: bool = Field(True, alias="isActive")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class AuthSession(BaseModel):
    """Auth session model."""
    id: str
    user_id: str = Field(alias="userId")
    ip_address: Optional[str] = Field(None, alias="ipAddress")
    user_agent: Optional[str] = Field(None, alias="userAgent")
    device_type: Optional[str] = Field(None, alias="deviceType")
    created_at: str = Field(alias="createdAt")
    last_active_at: str = Field(alias="lastActiveAt")
    expires_at: str = Field(alias="expiresAt")


class AuthMfaFactor(BaseModel):
    """MFA factor model."""
    id: str
    type: str
    name: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    email: Optional[str] = None
    is_primary: bool = Field(False, alias="isPrimary")
    created_at: str = Field(alias="createdAt")
    last_used_at: Optional[str] = Field(None, alias="lastUsedAt")


class AuthTotpEnrollment(BaseModel):
    """TOTP enrollment response."""
    secret: str
    qr_code_uri: str = Field(alias="qrCodeUri")


class AuthConnection(BaseModel):
    """SSO connection model."""
    id: str
    name: str
    type: str
    provider: str
    config: Dict[str, Any]
    domains: List[str] = Field(default_factory=list)
    domain_verified: bool = Field(False, alias="domainVerified")
    jit_provisioning: bool = Field(False, alias="jitProvisioning")
    default_role: Optional[str] = Field(None, alias="defaultRole")
    organization_id: Optional[str] = Field(None, alias="organizationId")
    is_active: bool = Field(True, alias="isActive")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class AuthOrganization(BaseModel):
    """Auth organization model."""
    id: str
    name: str
    slug: str
    display_name: Optional[str] = Field(None, alias="displayName")
    external_id: Optional[str] = Field(None, alias="externalId")
    logo: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    member_limit: Optional[int] = Field(None, alias="memberLimit")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class AuthOrganizationList(BaseModel):
    """List organizations response."""
    total_count: int = Field(alias="totalCount")
    organizations: List[AuthOrganization]


class AuthOrgMember(BaseModel):
    """Organization member model."""
    user_id: str = Field(alias="userId")
    user: AuthUser
    role: str
    permissions: List[str] = Field(default_factory=list)
    invited_by: Optional[str] = Field(None, alias="invitedBy")
    joined_at: str = Field(alias="joinedAt")


class AuthOrgInvitation(BaseModel):
    """Organization invitation model."""
    id: str
    email: str
    role: str
    status: str
    token: str
    expires_at: str = Field(alias="expiresAt")
    invited_by: str = Field(alias="invitedBy")
    created_at: str = Field(alias="createdAt")
    accepted_at: Optional[str] = Field(None, alias="acceptedAt")


class AuthWebhook(BaseModel):
    """Auth webhook model."""
    id: str
    url: str
    secret: str
    events: List[str]
    headers: Optional[Dict[str, str]] = None
    is_active: bool = Field(True, alias="isActive")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")


class AuthWebhookDelivery(BaseModel):
    """Webhook delivery model."""
    id: str
    webhook_id: str = Field(alias="webhookId")
    event_type: str = Field(alias="eventType")
    payload: Dict[str, Any]
    status: str
    attempt_count: int = Field(alias="attemptCount")
    response_status: Optional[int] = Field(None, alias="responseStatus")
    response_body: Optional[str] = Field(None, alias="responseBody")
    error: Optional[str] = None
    created_at: str = Field(alias="createdAt")
    delivered_at: Optional[str] = Field(None, alias="deliveredAt")


class AuthPasswordPolicy(BaseModel):
    """Password policy model."""
    min_length: int = Field(8, alias="minLength")
    max_length: int = Field(128, alias="maxLength")
    require_uppercase: bool = Field(False, alias="requireUppercase")
    require_lowercase: bool = Field(False, alias="requireLowercase")
    require_numbers: bool = Field(False, alias="requireNumbers")
    require_symbols: bool = Field(False, alias="requireSymbols")
    check_breached: bool = Field(False, alias="checkBreached")
    prevent_reuse: int = Field(0, alias="preventReuse")


class AuthBruteForcePolicy(BaseModel):
    """Brute force protection policy."""
    enabled: bool = True
    max_attempts: int = Field(5, alias="maxAttempts")
    lockout_duration: int = Field(15, alias="lockoutDuration")
    tracking_window: int = Field(10, alias="trackingWindow")
    ip_based_tracking: bool = Field(True, alias="ipBasedTracking")
    user_based_tracking: bool = Field(True, alias="userBasedTracking")


class AuthSessionPolicy(BaseModel):
    """Session policy model."""
    max_concurrent: int = Field(0, alias="maxConcurrent")
    idle_timeout: int = Field(60, alias="idleTimeout")
    absolute_timeout: int = Field(0, alias="absoluteTimeout")
    invalidate_on_password_change: bool = Field(True, alias="invalidateOnPasswordChange")


class AuthAuditLog(BaseModel):
    """Audit log entry model."""
    id: str
    event_type: str = Field(alias="eventType")
    user_id: Optional[str] = Field(None, alias="userId")
    resource_type: Optional[str] = Field(None, alias="resourceType")
    resource_id: Optional[str] = Field(None, alias="resourceId")
    ip_address: Optional[str] = Field(None, alias="ipAddress")
    user_agent: Optional[str] = Field(None, alias="userAgent")
    details: Optional[Dict[str, Any]] = None
    timestamp: str


class AuthAuditLogList(BaseModel):
    """Query audit logs response."""
    total_count: int = Field(alias="totalCount")
    logs: List[AuthAuditLog]


class LockoutStatus(BaseModel):
    """User lockout status."""
    is_locked: bool = Field(alias="isLocked")
    failed_attempts: int = Field(alias="failedAttempts")
    unlocks_at: Optional[str] = Field(None, alias="unlocksAt")


# ===========================================
# RESOURCES
# ===========================================

class AuthUsers:
    """Auth Users resource for managing end users."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        email: str,
        password: Optional[str] = None,
        email_verified: bool = False,
        phone: Optional[str] = None,
        phone_verified: bool = False,
        external_id: Optional[str] = None,
        profile: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        app_metadata: Optional[Dict[str, Any]] = None,
    ) -> AuthUser:
        """Create a new user."""
        data = {
            "email": email,
            "emailVerified": email_verified,
            "phoneVerified": phone_verified,
        }
        if password:
            data["password"] = password
        if phone:
            data["phone"] = phone
        if external_id:
            data["externalId"] = external_id
        if profile:
            data["profile"] = profile
        if metadata:
            data["metadata"] = metadata
        if app_metadata:
            data["appMetadata"] = app_metadata

        response = self._client._request("POST", "/auth/users", json=data)
        return AuthUser(**response)

    def list(
        self,
        count: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> AuthUserList:
        """List users with optional filtering."""
        params = {}
        if count is not None:
            params["count"] = count
        if offset is not None:
            params["offset"] = offset
        if status:
            params["status"] = status
        if search:
            params["search"] = search

        response = self._client._request("GET", "/auth/users", params=params)
        return AuthUserList(**response)

    def get(self, user_id: str) -> AuthUser:
        """Get a user by ID."""
        response = self._client._request("GET", f"/auth/users/{user_id}")
        return AuthUser(**response)

    def update(
        self,
        user_id: str,
        email: Optional[str] = None,
        email_verified: Optional[bool] = None,
        phone: Optional[str] = None,
        phone_verified: Optional[bool] = None,
        external_id: Optional[str] = None,
        profile: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        app_metadata: Optional[Dict[str, Any]] = None,
    ) -> AuthUser:
        """Update a user."""
        data = {}
        if email is not None:
            data["email"] = email
        if email_verified is not None:
            data["emailVerified"] = email_verified
        if phone is not None:
            data["phone"] = phone
        if phone_verified is not None:
            data["phoneVerified"] = phone_verified
        if external_id is not None:
            data["externalId"] = external_id
        if profile is not None:
            data["profile"] = profile
        if metadata is not None:
            data["metadata"] = metadata
        if app_metadata is not None:
            data["appMetadata"] = app_metadata

        response = self._client._request("PATCH", f"/auth/users/{user_id}", json=data)
        return AuthUser(**response)

    def delete(self, user_id: str) -> None:
        """Delete a user."""
        self._client._request("DELETE", f"/auth/users/{user_id}")

    def block(self, user_id: str) -> AuthUser:
        """Block a user account."""
        response = self._client._request("POST", f"/auth/users/{user_id}/block")
        return AuthUser(**response)

    def unblock(self, user_id: str) -> AuthUser:
        """Unblock a user account."""
        response = self._client._request("POST", f"/auth/users/{user_id}/unblock")
        return AuthUser(**response)

    def send_verification_email(self, user_id: str) -> None:
        """Send verification email to user."""
        self._client._request("POST", f"/auth/users/{user_id}/send-verification-email")

    def change_password(self, user_id: str, new_password: str) -> None:
        """Change user password."""
        self._client._request(
            "POST",
            f"/auth/users/{user_id}/change-password",
            json={"newPassword": new_password}
        )


class AuthApplications:
    """Auth Applications resource for managing OAuth applications."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        name: str,
        type: str,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
        redirect_uris: Optional[List[str]] = None,
        allowed_origins: Optional[List[str]] = None,
        logout_uris: Optional[List[str]] = None,
        grant_types: Optional[List[str]] = None,
        response_types: Optional[List[str]] = None,
    ) -> AuthApplication:
        """Create a new application."""
        data = {"name": name, "type": type}
        if description:
            data["description"] = description
        if logo_url:
            data["logoUrl"] = logo_url
        if redirect_uris:
            data["redirectUris"] = redirect_uris
        if allowed_origins:
            data["allowedOrigins"] = allowed_origins
        if logout_uris:
            data["logoutUris"] = logout_uris
        if grant_types:
            data["grantTypes"] = grant_types
        if response_types:
            data["responseTypes"] = response_types

        response = self._client._request("POST", "/auth/applications", json=data)
        return AuthApplication(**response)

    def list(self) -> List[AuthApplication]:
        """List all applications."""
        response = self._client._request("GET", "/auth/applications")
        return [AuthApplication(**app) for app in response]

    def get(self, application_id: str) -> AuthApplication:
        """Get an application by ID."""
        response = self._client._request("GET", f"/auth/applications/{application_id}")
        return AuthApplication(**response)

    def update(self, application_id: str, **kwargs) -> AuthApplication:
        """Update an application."""
        # Convert Python snake_case to camelCase
        data = {}
        key_mapping = {
            "name": "name",
            "description": "description",
            "logo_url": "logoUrl",
            "redirect_uris": "redirectUris",
            "allowed_origins": "allowedOrigins",
            "logout_uris": "logoutUris",
            "grant_types": "grantTypes",
            "response_types": "responseTypes",
            "is_active": "isActive",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", f"/auth/applications/{application_id}", json=data)
        return AuthApplication(**response)

    def delete(self, application_id: str) -> None:
        """Delete an application."""
        self._client._request("DELETE", f"/auth/applications/{application_id}")

    def rotate_secret(self, application_id: str) -> AuthApplication:
        """Rotate application client secret."""
        response = self._client._request("POST", f"/auth/applications/{application_id}/rotate-secret")
        return AuthApplication(**response)


class AuthSessions:
    """Auth Sessions resource for managing user sessions."""

    def __init__(self, client):
        self._client = client

    def list(self, user_id: str) -> List[AuthSession]:
        """List sessions for a user."""
        response = self._client._request("GET", f"/auth/users/{user_id}/sessions")
        return [AuthSession(**session) for session in response]

    def revoke(self, session_id: str) -> None:
        """Revoke a specific session."""
        self._client._request("DELETE", f"/auth/sessions/{session_id}")

    def revoke_all(self, user_id: str) -> None:
        """Revoke all sessions for a user."""
        self._client._request("DELETE", f"/auth/users/{user_id}/sessions")


class AuthMfa:
    """Auth MFA resource for managing multi-factor authentication."""

    def __init__(self, client):
        self._client = client

    def list_factors(self, user_id: str) -> List[AuthMfaFactor]:
        """List MFA factors for a user."""
        response = self._client._request("GET", f"/auth/users/{user_id}/mfa/factors")
        return [AuthMfaFactor(**factor) for factor in response]

    def enroll_totp(self, user_id: str) -> AuthTotpEnrollment:
        """Enroll TOTP factor for a user."""
        response = self._client._request("POST", f"/auth/users/{user_id}/mfa/totp/enroll")
        return AuthTotpEnrollment(**response)

    def verify_totp(self, user_id: str, code: str) -> AuthMfaFactor:
        """Verify and confirm TOTP enrollment."""
        response = self._client._request(
            "POST",
            f"/auth/users/{user_id}/mfa/totp/verify",
            json={"code": code}
        )
        return AuthMfaFactor(**response)

    def remove_factor(self, user_id: str, factor_id: str) -> None:
        """Remove an MFA factor."""
        self._client._request("DELETE", f"/auth/users/{user_id}/mfa/factors/{factor_id}")

    def generate_recovery_codes(self, user_id: str) -> List[str]:
        """Generate new recovery codes."""
        response = self._client._request("POST", f"/auth/users/{user_id}/mfa/recovery-codes")
        return response.get("codes", [])


class AuthConnections:
    """Auth Connections resource for managing SSO connections."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        name: str,
        type: str,
        config: Dict[str, Any],
        provider: Optional[str] = None,
        domains: Optional[List[str]] = None,
        jit_provisioning: bool = False,
        default_role: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> AuthConnection:
        """Create a new SSO connection."""
        data = {"name": name, "type": type, "config": config}
        if provider:
            data["provider"] = provider
        if domains:
            data["domains"] = domains
        if jit_provisioning:
            data["jitProvisioning"] = jit_provisioning
        if default_role:
            data["defaultRole"] = default_role
        if organization_id:
            data["organizationId"] = organization_id

        response = self._client._request("POST", "/auth/connections", json=data)
        return AuthConnection(**response)

    def list(self) -> List[AuthConnection]:
        """List all SSO connections."""
        response = self._client._request("GET", "/auth/connections")
        return [AuthConnection(**conn) for conn in response]

    def get(self, connection_id: str) -> AuthConnection:
        """Get an SSO connection by ID."""
        response = self._client._request("GET", f"/auth/connections/{connection_id}")
        return AuthConnection(**response)

    def update(self, connection_id: str, **kwargs) -> AuthConnection:
        """Update an SSO connection."""
        data = {}
        key_mapping = {
            "name": "name",
            "config": "config",
            "domains": "domains",
            "jit_provisioning": "jitProvisioning",
            "default_role": "defaultRole",
            "is_active": "isActive",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", f"/auth/connections/{connection_id}", json=data)
        return AuthConnection(**response)

    def delete(self, connection_id: str) -> None:
        """Delete an SSO connection."""
        self._client._request("DELETE", f"/auth/connections/{connection_id}")


class AuthOrganizations:
    """Auth Organizations resource for B2B multi-tenancy."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        name: str,
        slug: str,
        display_name: Optional[str] = None,
        external_id: Optional[str] = None,
        logo: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        member_limit: Optional[int] = None,
    ) -> AuthOrganization:
        """Create a new organization."""
        data = {"name": name, "slug": slug}
        if display_name:
            data["displayName"] = display_name
        if external_id:
            data["externalId"] = external_id
        if logo:
            data["logo"] = logo
        if metadata:
            data["metadata"] = metadata
        if member_limit is not None:
            data["memberLimit"] = member_limit

        response = self._client._request("POST", "/auth/organizations", json=data)
        return AuthOrganization(**response)

    def list(
        self,
        count: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
    ) -> AuthOrganizationList:
        """List organizations with optional filtering."""
        params = {}
        if count is not None:
            params["count"] = count
        if offset is not None:
            params["offset"] = offset
        if search:
            params["search"] = search

        response = self._client._request("GET", "/auth/organizations", params=params)
        return AuthOrganizationList(**response)

    def get(self, organization_id: str) -> AuthOrganization:
        """Get an organization by ID."""
        response = self._client._request("GET", f"/auth/organizations/{organization_id}")
        return AuthOrganization(**response)

    def update(self, organization_id: str, **kwargs) -> AuthOrganization:
        """Update an organization."""
        data = {}
        key_mapping = {
            "name": "name",
            "display_name": "displayName",
            "external_id": "externalId",
            "logo": "logo",
            "metadata": "metadata",
            "member_limit": "memberLimit",
            "auto_join_domains": "autoJoinDomains",
            "auto_join_role": "autoJoinRole",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", f"/auth/organizations/{organization_id}", json=data)
        return AuthOrganization(**response)

    def delete(self, organization_id: str) -> None:
        """Delete an organization."""
        self._client._request("DELETE", f"/auth/organizations/{organization_id}")

    def list_members(self, organization_id: str) -> List[AuthOrgMember]:
        """List organization members."""
        response = self._client._request("GET", f"/auth/organizations/{organization_id}/members")
        return [AuthOrgMember(**member) for member in response]

    def add_member(self, organization_id: str, user_id: str, role: str) -> AuthOrgMember:
        """Add a member to organization."""
        response = self._client._request(
            "POST",
            f"/auth/organizations/{organization_id}/members",
            json={"userId": user_id, "role": role}
        )
        return AuthOrgMember(**response)

    def update_member(self, organization_id: str, user_id: str, role: str) -> AuthOrgMember:
        """Update member role."""
        response = self._client._request(
            "PATCH",
            f"/auth/organizations/{organization_id}/members/{user_id}",
            json={"role": role}
        )
        return AuthOrgMember(**response)

    def remove_member(self, organization_id: str, user_id: str) -> None:
        """Remove a member from organization."""
        self._client._request("DELETE", f"/auth/organizations/{organization_id}/members/{user_id}")

    def list_invitations(self, organization_id: str) -> List[AuthOrgInvitation]:
        """List organization invitations."""
        response = self._client._request("GET", f"/auth/organizations/{organization_id}/invitations")
        return [AuthOrgInvitation(**inv) for inv in response]

    def invite(self, organization_id: str, email: str, role: str) -> AuthOrgInvitation:
        """Invite a user to organization."""
        response = self._client._request(
            "POST",
            f"/auth/organizations/{organization_id}/invitations",
            json={"email": email, "role": role}
        )
        return AuthOrgInvitation(**response)

    def revoke_invitation(self, organization_id: str, invitation_id: str) -> None:
        """Revoke an invitation."""
        self._client._request(
            "DELETE",
            f"/auth/organizations/{organization_id}/invitations/{invitation_id}"
        )


class AuthWebhooks:
    """Auth Webhooks resource for managing auth event webhooks."""

    def __init__(self, client):
        self._client = client

    def create(
        self,
        url: str,
        events: List[str],
        headers: Optional[Dict[str, str]] = None,
    ) -> AuthWebhook:
        """Create a new webhook."""
        data = {"url": url, "events": events}
        if headers:
            data["headers"] = headers

        response = self._client._request("POST", "/auth/webhooks", json=data)
        return AuthWebhook(**response)

    def list(self) -> List[AuthWebhook]:
        """List all webhooks."""
        response = self._client._request("GET", "/auth/webhooks")
        return [AuthWebhook(**wh) for wh in response]

    def get(self, webhook_id: str) -> AuthWebhook:
        """Get a webhook by ID."""
        response = self._client._request("GET", f"/auth/webhooks/{webhook_id}")
        return AuthWebhook(**response)

    def update(self, webhook_id: str, **kwargs) -> AuthWebhook:
        """Update a webhook."""
        data = {}
        key_mapping = {
            "url": "url",
            "events": "events",
            "headers": "headers",
            "is_active": "isActive",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", f"/auth/webhooks/{webhook_id}", json=data)
        return AuthWebhook(**response)

    def delete(self, webhook_id: str) -> None:
        """Delete a webhook."""
        self._client._request("DELETE", f"/auth/webhooks/{webhook_id}")

    def rotate_secret(self, webhook_id: str) -> str:
        """Rotate webhook secret."""
        response = self._client._request("POST", f"/auth/webhooks/{webhook_id}/rotate-secret")
        return response.get("secret", "")

    def list_deliveries(
        self,
        webhook_id: str,
        status: Optional[str] = None,
        count: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[AuthWebhookDelivery]:
        """List webhook deliveries."""
        params = {}
        if status:
            params["status"] = status
        if count is not None:
            params["count"] = count
        if offset is not None:
            params["offset"] = offset

        response = self._client._request(
            "GET",
            f"/auth/webhooks/{webhook_id}/deliveries",
            params=params
        )
        return [AuthWebhookDelivery(**d) for d in response]

    def retry_delivery(self, delivery_id: str) -> AuthWebhookDelivery:
        """Retry a webhook delivery."""
        response = self._client._request("POST", f"/auth/webhooks/deliveries/{delivery_id}/retry")
        return AuthWebhookDelivery(**response)

    def test(self, webhook_id: str, event_type: str) -> None:
        """Send a test event to webhook."""
        self._client._request(
            "POST",
            f"/auth/webhooks/{webhook_id}/test",
            json={"eventType": event_type}
        )


class AuthSecurity:
    """Auth Security resource for managing security policies."""

    def __init__(self, client):
        self._client = client

    def get_password_policy(self) -> AuthPasswordPolicy:
        """Get password policy."""
        response = self._client._request("GET", "/auth/security/password-policy")
        return AuthPasswordPolicy(**response)

    def update_password_policy(self, **kwargs) -> AuthPasswordPolicy:
        """Update password policy."""
        data = {}
        key_mapping = {
            "min_length": "minLength",
            "max_length": "maxLength",
            "require_uppercase": "requireUppercase",
            "require_lowercase": "requireLowercase",
            "require_numbers": "requireNumbers",
            "require_symbols": "requireSymbols",
            "check_breached": "checkBreached",
            "prevent_reuse": "preventReuse",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", "/auth/security/password-policy", json=data)
        return AuthPasswordPolicy(**response)

    def get_brute_force_policy(self) -> AuthBruteForcePolicy:
        """Get brute force protection policy."""
        response = self._client._request("GET", "/auth/security/brute-force-policy")
        return AuthBruteForcePolicy(**response)

    def update_brute_force_policy(self, **kwargs) -> AuthBruteForcePolicy:
        """Update brute force protection policy."""
        data = {}
        key_mapping = {
            "enabled": "enabled",
            "max_attempts": "maxAttempts",
            "lockout_duration": "lockoutDuration",
            "tracking_window": "trackingWindow",
            "ip_based_tracking": "ipBasedTracking",
            "user_based_tracking": "userBasedTracking",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", "/auth/security/brute-force-policy", json=data)
        return AuthBruteForcePolicy(**response)

    def get_session_policy(self) -> AuthSessionPolicy:
        """Get session policy."""
        response = self._client._request("GET", "/auth/security/session-policy")
        return AuthSessionPolicy(**response)

    def update_session_policy(self, **kwargs) -> AuthSessionPolicy:
        """Update session policy."""
        data = {}
        key_mapping = {
            "max_concurrent": "maxConcurrent",
            "idle_timeout": "idleTimeout",
            "absolute_timeout": "absoluteTimeout",
            "invalidate_on_password_change": "invalidateOnPasswordChange",
        }
        for key, value in kwargs.items():
            if key in key_mapping and value is not None:
                data[key_mapping[key]] = value

        response = self._client._request("PATCH", "/auth/security/session-policy", json=data)
        return AuthSessionPolicy(**response)

    def get_lockout_status(self, user_id: str) -> LockoutStatus:
        """Get lockout status for a user."""
        response = self._client._request("GET", f"/auth/security/lockout-status/{user_id}")
        return LockoutStatus(**response)

    def unlock_user(self, user_id: str) -> None:
        """Manually unlock a user."""
        self._client._request("POST", f"/auth/security/unlock/{user_id}")


class AuthLogs:
    """Auth Logs resource for querying audit logs."""

    def __init__(self, client):
        self._client = client

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        event_types: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        count: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> AuthAuditLogList:
        """Query audit logs."""
        params = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if event_types:
            params["eventTypes"] = event_types
        if user_id:
            params["userId"] = user_id
        if count is not None:
            params["count"] = count
        if offset is not None:
            params["offset"] = offset

        response = self._client._request("GET", "/auth/logs", params=params)
        return AuthAuditLogList(**response)

    def get(self, log_id: str) -> AuthAuditLog:
        """Get a specific audit log entry."""
        response = self._client._request("GET", f"/auth/logs/{log_id}")
        return AuthAuditLog(**response)

    def export(
        self,
        format: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
        """Export audit logs. Returns download URL."""
        data = {"format": format}
        if start_date:
            data["startDate"] = start_date
        if end_date:
            data["endDate"] = end_date

        response = self._client._request("POST", "/auth/logs/export", json=data)
        return response.get("url", "")


class Auth:
    """Main Auth resource that aggregates all auth sub-resources."""

    def __init__(self, client):
        self.users = AuthUsers(client)
        self.applications = AuthApplications(client)
        self.sessions = AuthSessions(client)
        self.mfa = AuthMfa(client)
        self.connections = AuthConnections(client)
        self.organizations = AuthOrganizations(client)
        self.webhooks = AuthWebhooks(client)
        self.security = AuthSecurity(client)
        self.logs = AuthLogs(client)
