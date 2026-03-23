"""
Email utility - offer to send output to user via email.
Uses SMTP (Gmail, Outlook, etc.). Set EMAIL_SENDER and EMAIL_APP_PASSWORD in .env.
"""
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def _looks_like_email(s: str) -> bool:
    """Basic format check: has @ and non-empty local + domain."""
    if not s or "@" not in s:
        return False
    parts = s.split("@", 1)
    return len(parts) == 2 and len(parts[0].strip()) > 0 and "." in parts[1] and len(parts[1].strip()) > 0


def offer_email_output(
    content: str,
    subject: str,
    attachment_content: bytes | str | None = None,
    attachment_filename: str | None = None,
) -> None:
    """
    Ask user if they want the output emailed. If yes, collect email and send.
    Optional: attachment_content + attachment_filename add a .ics (or other) file.
    When opened, .ics files add the event to the recipient's calendar.
    Requires EMAIL_SENDER and EMAIL_APP_PASSWORD in .env (Gmail app password, etc.).
    """
    while True:
        response = input("\nWould you like this output emailed to you? (y/n): ").strip().lower()
        if response in ("y", "yes"):
            break
        if response in ("n", "no"):
            return
        print("Please enter y or n.")

    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_APP_PASSWORD")
    if not sender or not password:
        print("Email not configured. Add EMAIL_SENDER and EMAIL_APP_PASSWORD to your .env file.")
        print("(Gmail: use an App Password from google.com/accountsecurity)")
        return

    while True:
        recipient = input("Enter your email address: ").strip()
        if _looks_like_email(recipient):
            break
        print("Invalid email address. Use format: name@domain.com")

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(content, "plain"))

        if attachment_content is not None and attachment_filename:
            if isinstance(attachment_content, str):
                attachment_content = attachment_content.encode("utf-8")
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_content)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{attachment_filename}"',
            )
            if attachment_filename.lower().endswith(".ics"):
                part.set_type("text/calendar")
            msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())

        print(f"Email sent to {recipient}")
    except smtplib.SMTPAuthenticationError:
        print("Email failed: authentication error. Check EMAIL_SENDER and EMAIL_APP_PASSWORD.")
    except Exception as e:
        print(f"Email failed: {e}")
