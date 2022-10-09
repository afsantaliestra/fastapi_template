"""{{cookiecutter.project_name}} - Domain - Infrastructure - SMTP Client"""  # pylint: disable=duplicate-code
from abc import ABC, abstractmethod
from typing import List


class ABCSMTPClient(ABC):
    """ABC SMTP Client"""

    @abstractmethod
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        port: int,
        tls: bool,
    ):
        """Init"""

    @abstractmethod
    async def send_email(
        self,
        email_to: List[str],
        subject: str = "",
        text: str = "",
        text_type="plain",
        **params,
    ) -> None:
        """Send email"""
