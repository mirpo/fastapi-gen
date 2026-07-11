import keyword
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

_EXCLUDE_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    ".git",
    "uv.lock",
}

_REPLACEABLE_SUFFIXES = {".py", ".toml", ".md", ""}


def is_valid_name(name) -> bool:
    # The name becomes the Python package, so it must be an importable module name
    return name.isascii() and name.isidentifier() and not keyword.iskeyword(name)


def discover_templates(templates_root: Path) -> dict[str, tuple[Path, str]]:
    templates = {}
    for d in sorted(templates_root.iterdir()):
        if not d.is_dir() or not d.name.startswith("template-"):
            continue
        src_dir = d / "src"
        if not src_dir.exists():
            continue
        modules = [p for p in src_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
        if len(modules) != 1:
            continue
        cli_name = d.name.removeprefix("template-").replace("-", "_")
        templates[cli_name] = (d, modules[0].name)
    return templates


def copy_template(template_dir: Path, dest_path: Path):
    def ignore_function(_directory, contents):
        return [name for name in contents if name in _EXCLUDE_PATTERNS]

    for item in template_dir.iterdir():
        if item.name in _EXCLUDE_PATTERNS:
            continue
        dest_item = dest_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest_item, ignore=ignore_function, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest_item)


def rename_package_in_pyproject(pyproject_path: Path, new_name: str):
    content = pyproject_path.read_text()
    content = re.sub(r'name\s*=\s*"[^"]+', f'name = "{new_name}', content, count=1)
    pyproject_path.write_text(content)


def replace_module_references(dest_path: Path, old_module: str, new_module: str):
    old_src = dest_path / "src" / old_module
    if old_src.exists():
        old_src.rename(dest_path / "src" / new_module)

    for path in dest_path.rglob("*"):
        if not path.is_file() or path.suffix not in _REPLACEABLE_SUFFIXES:
            continue
        content = path.read_text()
        updated = content.replace(f"{old_module}.", f"{new_module}.")
        updated = updated.replace(f"{old_module}/", f"{new_module}/")
        updated = updated.replace(f"import {old_module}", f"import {new_module}")
        updated = updated.replace(f"src/{old_module}", f"src/{new_module}")
        if updated != content:
            path.write_text(updated)


def _get_templates_root() -> Path | None:
    try:
        installed = resources.files("cli").joinpath("templates")
        if Path(installed).exists():
            return Path(installed)
    except (FileNotFoundError, AttributeError, TypeError):
        pass
    dev_path = Path(__file__).parent.parent.parent / "packages"
    if dev_path.exists():
        return dev_path
    return None


def _build_cli():
    templates_root = _get_templates_root()
    available = discover_templates(templates_root) if templates_root else {}
    choices = sorted(available.keys())
    default = "hello_world" if "hello_world" in choices else (choices[0] if choices else None)

    @click.command()
    @click.option("-t", "--template", default=default, type=click.Choice(choices), help="template")
    @click.option(
        "-o", "--output-dir", default=None, type=click.Path(exists=True, file_okay=False), help="output directory"
    )
    @click.option("--no-git", is_flag=True, default=False, help="skip git init")
    @click.argument("name")
    @click.version_option(version=__version__, prog_name="fastapi-gen")
    def cli(name: str, template: str, output_dir: str | None, *, no_git: bool):
        """This script creates new FastAPI project with NAME using TEMPLATE."""
        if not is_valid_name(name):
            click.echo(
                f"Error. Invalid name {name}. "
                "Name must be a valid Python identifier: letters, digits and underscores, "
                "not starting with a digit and not a Python keyword."
            )
            sys.exit(1)

        click.echo(f"Creating new project: '{name}' using template '{template}'...")

        base = Path(output_dir) if output_dir else Path.cwd()
        dest_path = base / name
        if dest_path.exists():
            click.echo(f"Error. Folder {dest_path} already exists.")
            sys.exit(1)

        template_dir, template_module = available[template]

        dest_path.mkdir(parents=True)

        try:
            click.echo("Copying template files...")
            copy_template(template_dir, dest_path)

            click.echo(f"Renaming package to '{name}'...")
            pyproject_path = dest_path / "pyproject.toml"
            if pyproject_path.exists():
                rename_package_in_pyproject(pyproject_path, name)

            replace_module_references(dest_path, template_module, name)
        except Exception as exc:  # noqa: BLE001 - clean up whatever failed, then report it
            shutil.rmtree(dest_path, ignore_errors=True)
            click.echo(f"Error. Project generation failed: {exc}. Removed incomplete {dest_path}.")
            sys.exit(1)

        if not no_git:
            git_result = subprocess.run(["git", "init"], cwd=dest_path, capture_output=True)  # noqa: PLW1510
            if git_result.returncode != 0:
                click.echo("Warning: git init failed; continuing without a git repository.")

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

    return cli


main = _build_cli()

if __name__ == "__main__":
    sys.exit(main())
