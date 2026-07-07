"""
Real outbound integrations (Slack + email).

This addresses Darwinbox's "few integrations" weakness by showing a real,
configurable connector — not a fake print statement.

How it works:
  - If you set a Slack webhook URL or SMTP email credentials via environment
    variables, the message is ACTUALLY sent.
  - If you set nothing, it safely falls back to a simulated send, so the demo
    still runs anywhere with zero setup.

Environment variables (all optional):
  SLACK_WEBHOOK_URL   -> if set, posts the message to that Slack channel
  SMTP_HOST           -> e.g. "smtp.gmail.com"
  SMTP_PORT           -> e.g. "587"
  SMTP_USER           -> your email login
  SMTP_PASSWORD       -> your email/app password
  SMTP_FROM           -> the "from" address (defaults to SMTP_USER)
"""

import os
import json
import smtplib
import urllib.request
from email.message import EmailMessage


def send_slack(message: str) -> str | None:
    """Post to Slack if SLACK_WEBHOOK_URL is configured. Returns a status string or None."""
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
        return None
    try:
        data = json.dumps({"text": message}).encode("utf-8")
        req = urllib.request.Request(
            webhook, data=data, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return "Sent via Slack webhook."
            return f"Slack responded with status {resp.status}."
    except Exception as exc:  # keep the agent resilient
        return f"Slack send failed: {exc}"


def send_email(to_address: str, subject: str, body: str) -> str | None:
    """Send an email if SMTP_* env vars are configured. Returns a status string or None."""
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    if not (host and user and password):
        return None
    port = int(os.environ.get("SMTP_PORT", "587"))
    from_addr = os.environ.get("SMTP_FROM", user)
    try:
        msg = EmailMessage()
        msg["From"] = from_addr
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
        return f"Sent email to {to_address}."
    except Exception as exc:
        return f"Email send failed: {exc}"


def deliver(message: str, email_to: str | None = None, subject: str = "HR Notification") -> str:
    """Try real channels first (Slack, then email); fall back to a simulated send.

    Returns a human-readable status describing what happened.
    """
    # 1) Try Slack
    slack_status = send_slack(message)
    if slack_status:
        return f"✅ {slack_status}"

    # 2) Try email
    if email_to:
        email_status = send_email(email_to, subject, message)
        if email_status:
            return f"✅ {email_status}"

    # 3) Fallback: simulate (no credentials configured)
    return (
        "✅ (simulated — no Slack/email credentials configured) "
        f'Would send: "{message}"'
    )
