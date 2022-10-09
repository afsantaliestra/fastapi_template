"""{{cookiecutter.project_name}} - Infrastructure - SMTP Client"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

import aiosmtplib

from {{cookiecutter.project_slug}}.domain.infrastructure.smtp_client import ABCSMTPClient


class SMTPClient(ABCSMTPClient):
    """SMTP Client"""

    def __init__(
        self,
        sender: str,
        host: str,
        user: str,
        password: str,
        port: int,
        tls: bool,
    ):
        """Init"""
        self.sender = sender
        self.params = {
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "tls": tls,
        }

    async def send_email(
        self,
        email_to: List[str],
        subject: str = "",
        text: str = "",
        text_type="plain",
        **params,
    ) -> None:
        """Send email"""
        # Default Parameters
        to_cc = params.get("cc", [])
        to_bcc = params.get("bcc", [])
        mail_params = params.get("mail_params", self.params)

        # Prepare Message
        msg = MIMEMultipart()
        msg.preamble = subject
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = ", ".join(email_to)
        if len(to_cc):
            msg["Cc"] = ", ".join(to_cc)
        if len(to_bcc):
            msg["Bcc"] = ", ".join(to_bcc)

        msg.attach(MIMEText(text, text_type, "utf-8"))

        # Contact SMTP server and send Message
        host = mail_params.get("host", "localhost")
        is_ssl = mail_params.get("SSL", False)
        is_tls = mail_params.get("TLS", False)
        port = mail_params.get("port", 465 if is_ssl else 25)
        smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=is_ssl)

        await smtp.connect()
        if is_tls:
            await smtp.starttls()
        if "user" in mail_params:
            await smtp.login(mail_params["user"], mail_params["password"])
        await smtp.send_message(msg)
        await smtp.quit()
