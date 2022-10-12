"""FastAPI Template - Hooks - Post Gen Project"""
import subprocess


dependencies = [
    "uvicorn",
    "fastapi",
    "dependency-injector[yaml]",
    "toml",
    "python-jose[cryptography]",
    "python-multipart",
    "passlib",
    "pydantic[email]",
    "aiosmtplib",
]

dev_dependencies = [
    "black",
    "isort",
    "pylint",
    "bandit",
    "flake8",
    "pytest",
    "requests",
    "pytest-mock",
]


def setup_poetry_environment():
    """Setup poetry environment"""
    subprocess.run(["poetry", "init", "--name", "{{ cookiecutter.project_slug }}", "-n"])

    if dependencies:
        subprocess.run(["poetry", "add", *dependencies])

    subprocess.run(["poetry", "add", "--dev", *dev_dependencies])


def setup_git():
    """Setup git"""
    subprocess.run(["git", "init"], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "checkout", "-b", "develop"], stdout=subprocess.DEVNULL)


def format_code():
    """Format code"""
    subprocess.run(["make", "format"], stdout=subprocess.DEVNULL)


setup_poetry_environment()
setup_git()
format_code()
