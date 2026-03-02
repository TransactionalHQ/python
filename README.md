# Transactional Python SDK

[![PyPI version](https://badge.fury.io/py/usetransactional.svg)](https://pypi.org/project/usetransactional/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the Transactional API - Email, SMS, and Communication APIs.

## Installation

```bash
pip install transactional
```

## Quick Start

```python
from transactional import Transactional

# Initialize the client
client = Transactional(api_key="tr_live_xxxxx")

# Send an email
result = client.emails.send(
    from_email="sender@domain.com",
    to="recipient@example.com",
    subject="Hello!",
    html_body="<h1>Hello World</h1>",
)

print(result.message_id)
```

## Features

### Email

```python
# Send a single email
result = client.emails.send(
    from_email="sender@domain.com",
    to="recipient@example.com",
    subject="Hello!",
    html_body="<h1>Hello World</h1>",
    tag="welcome",
)

# Send with a template
result = client.emails.send_with_template(
    from_email="sender@domain.com",
    to="recipient@example.com",
    template_alias="welcome-email",
    template_model={"name": "John"},
)

# Send batch emails
results = client.emails.send_batch([
    {
        "from_email": "sender@domain.com",
        "to": "user1@example.com",
        "subject": "Hello User 1",
        "html_body": "<p>Hello!</p>",
    },
    {
        "from_email": "sender@domain.com",
        "to": "user2@example.com",
        "subject": "Hello User 2",
        "html_body": "<p>Hello!</p>",
    },
])
```

### SMS

```python
# Send a single SMS
result = client.sms.send(
    to="+14155551234",
    template_alias="otp-verification",
    template_model={"code": "123456"},
)

print(result.message_id)

# Send batch SMS
results = client.sms.send_batch([
    {
        "to": "+14155551234",
        "template_alias": "otp-verification",
        "template_model": {"code": "111111"},
    },
    {
        "to": "+14155555678",
        "template_alias": "otp-verification",
        "template_model": {"code": "222222"},
    },
])

# Check message status
message = client.sms.get("sms_abc123")
print(message.status)

# List inbound messages
inbound = client.sms.list_inbound(count=50)
for msg in inbound.messages:
    print(f"From {msg.from_number}: {msg.body}")
```

### Templates

```python
# List templates
templates = client.templates.list()

# Get a specific template
template = client.templates.get(template_id=123)

# Create a template
template = client.templates.create(
    name="Welcome Email",
    subject="Welcome, {{name}}!",
    html_body="<h1>Hello {{name}}</h1>",
)
```

### Suppressions

```python
# List email suppressions
suppressions = client.suppressions.list()

# Check if email is suppressed
result = client.suppressions.check("user@example.com")
if result.suppressed:
    print(f"Email is suppressed: {result.reason}")

# Add to suppression list
client.suppressions.add(
    email="user@example.com",
    reason="MANUAL",
)

# Remove from suppression list
client.suppressions.remove("user@example.com")
```

### Bounces

```python
# List bounces
bounces = client.bounces.list()

# Get bounce details
bounce = client.bounces.get(bounce_id=123)

# Activate a bounced email (allow sending again)
client.bounces.activate("user@example.com")
```

## Error Handling

```python
from transactional import Transactional
from transactional.errors import (
    TransactionalError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

client = Transactional(api_key="tr_live_xxxxx")

try:
    result = client.emails.send(
        from_email="sender@domain.com",
        to="recipient@example.com",
        subject="Hello!",
        html_body="<h1>Hello</h1>",
    )
except AuthenticationError as e:
    print(f"Invalid API key: {e}")
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after}")
except ValidationError as e:
    print(f"Validation error: {e}")
except TransactionalError as e:
    print(f"API error: {e}")
```

## Async Support

```python
import asyncio
from transactional import AsyncTransactional

async def main():
    client = AsyncTransactional(api_key="tr_live_xxxxx")

    result = await client.emails.send(
        from_email="sender@domain.com",
        to="recipient@example.com",
        subject="Hello!",
        html_body="<h1>Hello World</h1>",
    )

    print(result.message_id)

    await client.close()

asyncio.run(main())
```

## Configuration

```python
from transactional import Transactional

client = Transactional(
    api_key="tr_live_xxxxx",
    base_url="https://api.usetransactional.com",  # Custom base URL
    timeout=30.0,  # Request timeout in seconds
    retries=3,  # Number of retries for failed requests
)
```

## Documentation

Full documentation is available at [usetransactional.com/docs/getting-started](https://usetransactional.com/docs/getting-started/quick-start)

## License

MIT
