import os
import re
import shutil
import subprocess
import sys
from importlib import resources
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

try:
    __version__ = version("fastapi-gen")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

_pattern = r"^[a-zA-Z0-9_]+$"
_choices = ["hello_world", "advanced", "nlp", "langchain", "llama"]

# Template name mapping
_template_map = {
    "hello_world": ("template-hello-world", "hello_world"),
    "advanced": ("template-advanced", "advanced"),
    "nlp": ("template-nlp", "nlp"),
    "langchain": ("template-langchain", "langchain_app"),
    "llama": ("template-llama", "llama_app"),
}


def is_valid_name(name) -> bool:
    return re.match(_pattern, name) is not None


def copy_template(template_dir: Path, dest_path: Path):
    """Recursively copy template directory, excluding dev artifacts."""
    exclude_patterns = {
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "venv",
        ".git",
        "uv.lock",
    }

    def ignore_function(_directory, contents):
        """Custom ignore function that excludes dev artifacts but keeps other dotfiles."""
        return [name for name in contents if name in exclude_patterns]

    for item in template_dir.iterdir():
        if item.name in exclude_patterns:
            continue

        dest_item = dest_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest_item, ignore=ignore_function, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest_item)


def rename_package_in_pyproject(pyproject_path: Path, new_name: str):
    """Rename the package in pyproject.toml."""
    content = pyproject_path.read_text()

    # Replace name field
    content = re.sub(r'name\s*=\s*"[^"]+', f'name = "{new_name}', content, count=1)

    pyproject_path.write_text(content)


def update_scripts_in_pyproject(pyproject_path: Path, old_module: str, new_module: str):
    """Update script module names in pyproject.toml."""
    content = pyproject_path.read_text()

    # Replace module names in scripts
    content = content.replace(f"{old_module}.", f"{new_module}.")

    pyproject_path.write_text(content)


def rename_src_directory(dest_path: Path, old_name: str, new_name: str):
    """Rename the src/{old_name} directory to src/{new_name}."""
    old_src = dest_path / "src" / old_name
    new_src = dest_path / "src" / new_name

    if old_src.exists():
        old_src.rename(new_src)


def update_imports_in_tests(tests_dir: Path, old_module: str, new_module: str):
    """Update import statements in test files."""
    if not tests_dir.exists():
        return

    for test_file in tests_dir.glob("*.py"):
        if test_file.name == "__init__.py":
            continue

        content = test_file.read_text()
        content = content.replace(f"from {old_module}.", f"from {new_module}.")
        content = content.replace(f"import {old_module}", f"import {new_module}")
        test_file.write_text(content)


@click.command()
@click.option("-t", "--template", default="hello_world", type=click.Choice(_choices), help="template")
@click.argument("name")
@click.version_option(version=__version__, prog_name="fastapi-gen")
def main(name: str, template: str):
    """This script creates new FastAPI project with NAME using TEMPLATE."""
    if not is_valid_name(name):
        click.echo(f"Error. Invalid name {name}. Name must match: {_pattern}")
        sys.exit(1)

    click.echo(f"Creating new project: '{name}' using template '{template}'...")

    dest_path = Path.cwd() / name
    if dest_path.exists():
        click.echo(f"Error. Folder {dest_path} already exists.")
        sys.exit(1)

    # Get template info
    template_package_name, template_module_name = _template_map[template]

    # Get template directory - try installed package first, then development mode
    template_files = None
    try:
        # Try installed package location (cli/templates/)
        template_files = resources.files("cli").joinpath("templates").joinpath(template_package_name)
        if not Path(template_files).exists():
            template_files = None
    except (FileNotFoundError, AttributeError, TypeError):
        pass

    if template_files is None:
        # Try development mode location (packages/)
        dev_template_path = Path(__file__).parent.parent.parent / "packages" / template_package_name
        if dev_template_path.exists():
            template_files = dev_template_path
        else:
            click.echo(f"Error. Template {template} not found in installation or development mode.")
            sys.exit(1)

    # Create destination directory
    dest_path.mkdir(parents=True)

    # Copy template
    click.echo("Copying template files...")
    copy_template(Path(template_files), dest_path)

    # Rename package in pyproject.toml
    pyproject_path = dest_path / "pyproject.toml"
    if pyproject_path.exists():
        click.echo(f"Renaming package to '{name}'...")
        rename_package_in_pyproject(pyproject_path, name)
        update_scripts_in_pyproject(pyproject_path, template_module_name, name)

    # Rename src directory
    click.echo(f"Renaming module to '{name}'...")
    rename_src_directory(dest_path, template_module_name, name)

    # Update imports in tests
    tests_dir = dest_path / "tests"
    if tests_dir.exists():
        update_imports_in_tests(tests_dir, template_module_name, name)

    # Initialize git repository
    os.chdir(dest_path)
    subprocess.run(["git", "init"], capture_output=True)  # noqa: PLW1510

    # Success message
    welcome_message = f"""
{click.style("Success!", fg="green", bold=True)} Created {name} at {dest_path}

Inside that directory, you can run several commands:

    {click.style("make install", fg="blue", bold=True)}
    Install dependencies

    {click.style("make start", fg="blue", bold=True)}
    Start the development server

    {click.style("make test", fg="blue", bold=True)}
    Run tests

    {click.style("make lint", fg="blue", bold=True)}
    Run linter

We suggest that you begin by typing:

    {click.style(f"cd {name}", fg="blue", bold=True)}
    {click.style("make install", fg="blue", bold=True)}
    {click.style("make start", fg="blue", bold=True)}

Then open {click.style("http://localhost:8000/docs", fg="cyan")} to see your API.

{click.style("Happy hacking!", fg="yellow", blink=True, bold=True)}
"""
    click.echo(welcome_message)
    return 0


if __name__ == "__main__":
    sys.exit(main())
