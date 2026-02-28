"""
Transactional SDK Resources

API resource modules.
"""

from usetransactional.resources.base import BaseResource, AsyncBaseResource
from usetransactional.resources.emails import Emails, AsyncEmails
from usetransactional.resources.templates import Templates, AsyncTemplates
from usetransactional.resources.suppressions import Suppressions, AsyncSuppressions
from usetransactional.resources.bounces import Bounces, AsyncBounces
from usetransactional.resources.messages import Messages, AsyncMessages
from usetransactional.resources.stats import Stats, AsyncStats
from usetransactional.resources.sms import Sms, AsyncSms
from usetransactional.resources.forms import Forms, AsyncForms
from usetransactional.resources.support import Support, AsyncSupport

__all__ = [
    # Base
    "BaseResource",
    "AsyncBaseResource",
    # Email resources
    "Emails",
    "AsyncEmails",
    "Templates",
    "AsyncTemplates",
    "Suppressions",
    "AsyncSuppressions",
    "Bounces",
    "AsyncBounces",
    "Messages",
    "AsyncMessages",
    "Stats",
    "AsyncStats",
    # SMS resources
    "Sms",
    "AsyncSms",
    # Forms resources
    "Forms",
    "AsyncForms",
    # Support resources
    "Support",
    "AsyncSupport",
]
