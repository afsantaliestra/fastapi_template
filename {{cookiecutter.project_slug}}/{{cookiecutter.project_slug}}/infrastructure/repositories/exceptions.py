"""{{cookiecutter.project_name}} - Infrastructure - Repositories - Exceptions"""


class UserNotFoundException(Exception):
    """User Not Found Exception"""

    def __init__(
        self,
        username_or_email: str,
        code: int = None,
        message: str = None,
    ):
        """Init"""
        print(username_or_email, code, message)
        self.username_or_email = username_or_email
        self.code = code or 404
        self.message = message or "User ({username_or_email}) not found."
        super().__init__(message.format(username_or_email=self.username_or_email))
