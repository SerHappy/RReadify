from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from aiosmtplib import SMTP
from jinja2 import Template
from jose import jwt
from jose.exceptions import JWTError

from app.core.config import settings


async def send_email(
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    """Sends an email to the specified address."""
    email_message = MIMEMultipart("alternative")
    email_message["From"] = settings.EMAIL.FROM_EMAIL
    email_message["To"] = (
        settings.EMAIL.TEST_USER if settings.EMAIL.TEST_USER else email_to
    )
    email_message["Subject"] = subject

    email_message.attach(MIMEText(html_content, "html"))

    async with SMTP(
        hostname=settings.EMAIL.SMTP_HOST,
        port=settings.EMAIL.SMTP_PORT,
        use_tls=True,
    ) as smtp:
        await smtp.login(settings.EMAIL.SMTP_USER, settings.EMAIL.SMTP_PASSWORD)
        await smtp.send_message(email_message)


def generate_confirmation_email(token: str) -> str:
    """Generates an email with a confirmation link."""
    context = {
        "link": f"{settings.SECURITY.EMAIL_CONFIRM_URL}?token={token}",
    }
    return _render_email_template("verification_email.j2", context)


def generate_confirmation_token(email: str) -> str:
    """Generates a token for email confirmation."""
    delta = timedelta(seconds=settings.SECURITY.EMAIL_CONFIRMATION_EXPIRE)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    return jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "sub": email,
            "type": settings.SECURITY.EMAIL_TOKEN_TYPE,
        },
        settings.SECURITY.SECRET_KEY,
        algorithm=settings.SECURITY.ALGORITHM,
    )


def verify_email_token(token: str) -> str | None:
    """Verifies the email token."""
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECURITY.SECRET_KEY,
            algorithms=[settings.SECURITY.ALGORITHM],
        )
        token_type = decoded_token["type"]
        if token_type != settings.SECURITY.EMAIL_TOKEN_TYPE:
            return None
        email = decoded_token["sub"]
    except JWTError:
        return None
    else:
        return email


def _render_email_template(template_name: str, context: dict[str, Any]) -> str:
    """Render email template."""
    template_str = (
        Path(__file__).parent.parent / "templates" / template_name
    ).read_text()
    return Template(template_str).render(context)
