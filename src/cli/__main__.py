import os
import re
import subprocess
import sys
from importlib import resources
from importlib.metadata import PackageNotFoundError, version

import click

try:
    __version__ = version("fastapi-gen")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

_pattern = r"^[a-zA-Z0-9_]+$"


def is_valid_name(name) -> bool:
    return re.match(_pattern, name) is not None


def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path) as file:
        content = file.read()

    modified_content = content.replace(old_string, new_string)

    with open(file_path, "w") as file:
        file.write(modified_content)


_choices = ["hello_world", "advanced", "nlp", "langchain", "llama"]


def _create_dir(path: str):
    try:
        os.makedirs(path)
        click.echo(f"Folder '{path}' created successfully.")
    except OSError as e:
        click.echo(f"Error creating folder: {e}")


def _walk_resources(package: str, path: str = ""):
    for file in resources.files(package).iterdir():
        if file.name in ["__pycache__", ".pytest_cache", "venv"]:
            continue

        if file.is_dir() and file.name.startswith("."):
            continue

        if file.is_dir():
            _create_dir(os.path.join(path, file.name))
            _walk_resources(f"{package}.{file.name}", os.path.join(path, file.name))
        else:
            try:
                content = resources.read_text(package, file.name)
                with open(os.path.join(path, file.name), "w") as f:
                    f.write(content)
            except UnicodeDecodeError:
                content_bytes = resources.files(package).joinpath(file.name).read_bytes()
                with open(os.path.join(path, file.name), "wb") as f:
                    f.write(content_bytes)


@click.command()
@click.option("-t", "--template", default="hello_world", type=click.Choice(_choices), help="template")
@click.argument("name")
@click.version_option(version=__version__, prog_name="create-fast-api")
def fastapi_create(name: str, template: str):
    """This script creates new FastAPI project with NAME using TEMPLATE."""
    if not is_valid_name(name):
        click.echo(f"Error. Invalid name {name}. Name contain only: {_pattern}")
        sys.exit(1)

    click.echo(f"Creating new project: '{name}' using template '{template}'...")
    current_folder = os.getcwd()
    new_project_path = os.path.join(current_folder, name)
    os.path.join(current_folder, "src", "templates", template)

    if os.path.exists(new_project_path):
        click.echo(f"Error. Folder {new_project_path} already exists.")
        sys.exit(1)

    _create_dir(new_project_path)
    _walk_resources(f"templates.{template}", new_project_path)

    os.chdir(new_project_path)

    replace_string_in_file(os.path.join(new_project_path, "tests", "test_main.py"), f"src.templates.{template}", name)

    try:
        subprocess.run(["make", "init"], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"An error occurred while executing the Makefile: {e}")
        sys.exit(1)

    welcome_message = f"""
Success! Created new-app at {new_project_path}
Inside that directory, you can run several commands:

    {click.style("make start", bg="blue", fg="white")}
    Starts the development server.

    {click.style("make test", bg="blue", fg="white")}
    Starts the test runner.

    {click.style("make lint", bg="blue", fg="white")}
    Starts linters.

We suggest that you begin by typing:

    {click.style(f"cd {name}", bg="blue", fg="white")}
    {click.style("make start", bg="blue", fg="white")}

{click.style("Happy hacking!", blink=True, bold=True)}
"""
    click.echo(welcome_message)


sys.exit(fastapi_create())
