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

dev_dependencies = ["black", "isort", "pylint", "bandit", "flake8", "pytest"]


def setup_poetry_environment():
    subprocess.run(["poetry", "init", "--name", "{{ cookiecutter.project_slug }}", "-n"])

    if dependencies:
        subprocess.run(["poetry", "add", *dependencies])

    subprocess.run(["poetry", "add", "--dev", *dev_dependencies])


def setup_git():
    subprocess.run(["git", "init"], stdout=subprocess.DEVNULL)
    subprocess.run(["git", "checkout", "-b", "develop"], stdout=subprocess.DEVNULL)


setup_poetry_environment()
setup_git()
