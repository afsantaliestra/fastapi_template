"""{{cookiecutter.project_name}} - Domain - Infrastructure - SMTP Client"""  # pylint: disable=duplicate-code
from abc import ABC, abstractmethod


class BaseSMTPClient(ABC):
    """SMTP Client"""

    @abstractmethod
    def __init__(self, host: str, user: str, password: str, port: int, tls: bool):
        """Init"""

    @abstractmethod
    async def send_email(
        self,
        _email_to: str,
        subject: str = "",
        text: str = "",
        text_type="plain",
        **params,
    ) -> None:
        """Send email"""
