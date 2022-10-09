"""{{cookiecutter.project_name}} - Containers"""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import (
    Configuration,
    Container,
    DependenciesContainer,
    Singleton,
)

from {{cookiecutter.project_slug}}.application.services.login import LoginService
from {{cookiecutter.project_slug}}.application.services.token import TokenService
from {{cookiecutter.project_slug}}.application.services.user import UserService
from {{cookiecutter.project_slug}}.infrastructure.repositories.in_memory.users import UserRepository
from {{cookiecutter.project_slug}}.infrastructure.smtp_client import SMTPClient


class InfrastructureContainer(DeclarativeContainer):
    """Infrastructure Container"""

    config = Configuration()

    user_repository: UserRepository = Singleton(UserRepository)

    smtp_client: SMTPClient = Singleton(
        SMTPClient,
        sender=config.smtp_client.sender,
        host=config.smtp_client.host,
        user=config.smtp_client.user,
        password=config.smtp_client.password,
        port=config.smtp_client.port,
        tls=config.smtp_client.tls,
    )


class ServiceContainer(DeclarativeContainer):
    """Service Container"""

    infrastructures = DependenciesContainer()

    config = Configuration()

    token_service: TokenService = Singleton(
        TokenService,
        algorithm=config.token.algorithm,
        secret_key=config.token.secret_key,
        token_expiration=config.token.token_expiration,
        reset_password_token_expiration=config.token.reset_password_token_expiration,
    )
    user_service: UserService = Singleton(
        UserService,
        token_service=token_service,
        user_repository=infrastructures.user_repository,
    )
    login_service: LoginService = Singleton(
        LoginService,
        token_service=token_service,
        user_service=user_service,
        smtp_client=infrastructures.smtp_client,
    )


class ApplicationContainer(DeclarativeContainer):
    """Application Container"""

    config: Configuration = Configuration(yaml_files=["config.yaml"])

    wiring_config: WiringConfiguration = WiringConfiguration(
        packages=["{{cookiecutter.project_slug}}.gateway", "{{cookiecutter.project_slug}}.application"]
    )

    infrastructures: InfrastructureContainer = Container(
        InfrastructureContainer,
        config=config.infrastructure,
    )

    services: ServiceContainer = Container(
        ServiceContainer,
        infrastructures=infrastructures,
        config=config.service,
    )
