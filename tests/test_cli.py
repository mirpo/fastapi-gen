import os
import subprocess
import textwrap
from pathlib import Path

import pytest
from click.testing import CliRunner

from cli.__main__ import (
    copy_template,
    discover_templates,
    is_valid_name,
    main,
    rename_package_in_pyproject,
    replace_module_references,
)


class TestIsValidName:
    @pytest.mark.parametrize(
        "name",
        ["my_app", "app", "a", "MyApp123", "hello_world_2"],
    )
    def test_accepts_valid_names(self, name):
        assert is_valid_name(name)

    @pytest.mark.parametrize(
        "name",
        ["my-app", "my.app", "my app", "", "hello/world", "app@2", "café", "1app", "9lives", "class", "import"],
    )
    def test_rejects_invalid_names(self, name):
        assert not is_valid_name(name)


class TestCopyTemplate:
    def _make_template(self, tmp_path: Path) -> Path:
        tpl = tmp_path / "template"
        (tpl / "src" / "mymod").mkdir(parents=True)
        (tpl / "src" / "mymod" / "main.py").write_text("app = 1")
        (tpl / "pyproject.toml").write_text("[project]")
        (tpl / ".env_dev").write_text("KEY=val")
        (tpl / ".gitignore").write_text("*.pyc")
        (tpl / "__pycache__").mkdir()
        (tpl / "__pycache__" / "mod.cpython-312.pyc").write_bytes(b"\x00")
        (tpl / ".venv" / "bin").mkdir(parents=True)
        (tpl / ".venv" / "bin" / "python").write_text("")
        (tpl / "uv.lock").write_text("lock")
        (tpl / ".pytest_cache").mkdir()
        (tpl / ".ruff_cache").mkdir()
        return tpl

    def test_copies_source_files(self, tmp_path):
        tpl = self._make_template(tmp_path)
        dest = tmp_path / "output"
        dest.mkdir()

        copy_template(tpl, dest)

        assert (dest / "src" / "mymod" / "main.py").read_text() == "app = 1"
        assert (dest / "pyproject.toml").read_text() == "[project]"

    def test_copies_dotfiles(self, tmp_path):
        tpl = self._make_template(tmp_path)
        dest = tmp_path / "output"
        dest.mkdir()

        copy_template(tpl, dest)

        assert (dest / ".env_dev").exists()
        assert (dest / ".gitignore").exists()

    def test_excludes_dev_artifacts(self, tmp_path):
        tpl = self._make_template(tmp_path)
        dest = tmp_path / "output"
        dest.mkdir()

        copy_template(tpl, dest)

        assert not (dest / "__pycache__").exists()
        assert not (dest / ".venv").exists()
        assert not (dest / "uv.lock").exists()
        assert not (dest / ".pytest_cache").exists()
        assert not (dest / ".ruff_cache").exists()


class TestRenamePackageInPyproject:
    def test_replaces_package_name(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            textwrap.dedent("""\
            [project]
            name = "hello-world-app"
            version = "0.1.0"
            dependencies = ["fastapi==0.136.1"]
        """)
        )

        rename_package_in_pyproject(pyproject, "my_cool_app")

        content = pyproject.read_text()
        assert 'name = "my_cool_app"' in content

    def test_only_replaces_first_name_field(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            textwrap.dedent("""\
            [project]
            name = "old-app"
            dependencies = ["some-package-with-name==1.0"]

            [tool.other]
            name = "should-not-change"
        """)
        )

        rename_package_in_pyproject(pyproject, "new_app")

        content = pyproject.read_text()
        assert 'name = "new_app"' in content
        assert 'name = "should-not-change"' in content

    def test_preserves_rest_of_file(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        original = textwrap.dedent("""\
            [project]
            name = "old-app"
            version = "0.1.0"
            description = "My app"
        """)
        pyproject.write_text(original)

        rename_package_in_pyproject(pyproject, "new_app")

        content = pyproject.read_text()
        assert 'version = "0.1.0"' in content
        assert 'description = "My app"' in content


class TestDiscoverTemplates:
    def _make_templates_dir(self, tmp_path: Path) -> Path:
        tpl_root = tmp_path / "packages"

        for name, module in [
            ("template-hello-world", "hello_world"),
            ("template-nlp", "nlp"),
            ("template-llama", "llama_app"),
        ]:
            (tpl_root / name / "src" / module).mkdir(parents=True)
            (tpl_root / name / "src" / module / "__init__.py").write_text("")

        return tpl_root

    def test_discovers_all_templates(self, tmp_path):
        tpl_root = self._make_templates_dir(tmp_path)

        templates = discover_templates(tpl_root)

        assert "hello_world" in templates
        assert "nlp" in templates
        assert "llama" in templates

    def test_returns_correct_directory(self, tmp_path):
        tpl_root = self._make_templates_dir(tmp_path)

        templates = discover_templates(tpl_root)

        assert templates["hello_world"][0] == tpl_root / "template-hello-world"

    def test_discovers_module_name_from_src(self, tmp_path):
        tpl_root = self._make_templates_dir(tmp_path)

        templates = discover_templates(tpl_root)

        assert templates["hello_world"][1] == "hello_world"
        assert templates["llama"][1] == "llama_app"

    def test_ignores_non_template_dirs(self, tmp_path):
        tpl_root = self._make_templates_dir(tmp_path)
        (tpl_root / "some-other-package" / "src" / "foo").mkdir(parents=True)

        templates = discover_templates(tpl_root)

        assert "some_other_package" not in templates
        assert len(templates) == 3

    def test_empty_dir(self, tmp_path):
        tpl_root = tmp_path / "packages"
        tpl_root.mkdir()

        templates = discover_templates(tpl_root)

        assert templates == {}


class TestReplaceModuleReferences:
    def _make_project(self, tmp_path: Path, module_name: str = "nlp") -> Path:
        dest = tmp_path / "project"
        dest.mkdir()
        (dest / "src" / module_name).mkdir(parents=True)
        (dest / "src" / module_name / "main.py").write_text("app = 1")
        (dest / "tests").mkdir()
        (dest / "tests" / "test_main.py").write_text(f"from {module_name}.main import app\n")
        (dest / "Makefile").write_text(f"start:\n\tuvicorn {module_name}.main:app\n")
        (dest / "README.md").write_text(f"Run uvicorn {module_name}.main:app\nSee {module_name}/ dir\n")
        (dest / "pyproject.toml").write_text(
            f'[project]\nname = "old-name"\n\n[project.scripts]\nstart = "{module_name}.main:app"\n\n'
            f'[tool.hatch.build.targets.wheel]\npackages = ["src/{module_name}"]\n'
        )
        return dest

    def test_renames_src_directory(self, tmp_path):
        dest = self._make_project(tmp_path)

        replace_module_references(dest, "nlp", "my_app")

        assert (dest / "src" / "my_app" / "main.py").exists()
        assert not (dest / "src" / "nlp").exists()

    def test_updates_makefile(self, tmp_path):
        dest = self._make_project(tmp_path)

        replace_module_references(dest, "nlp", "my_app")

        assert "uvicorn my_app.main:app" in (dest / "Makefile").read_text()

    def test_updates_readme(self, tmp_path):
        dest = self._make_project(tmp_path)

        replace_module_references(dest, "nlp", "my_app")

        content = (dest / "README.md").read_text()
        assert "uvicorn my_app.main:app" in content
        assert "my_app/" in content

    def test_updates_test_imports(self, tmp_path):
        dest = self._make_project(tmp_path)

        replace_module_references(dest, "nlp", "my_app")

        assert "from my_app.main import app" in (dest / "tests" / "test_main.py").read_text()

    def test_updates_pyproject_scripts(self, tmp_path):
        dest = self._make_project(tmp_path)

        replace_module_references(dest, "nlp", "my_app")

        assert '"my_app.main:app"' in (dest / "pyproject.toml").read_text()

    def test_updates_hatch_wheel_packages_path(self, tmp_path):
        dest = self._make_project(tmp_path)

        replace_module_references(dest, "nlp", "my_app")

        content = (dest / "pyproject.toml").read_text()
        assert 'packages = ["src/my_app"]' in content
        assert "src/nlp" not in content

    def test_updates_bare_imports(self, tmp_path):
        dest = self._make_project(tmp_path)
        (dest / "tests" / "test_main.py").write_text("import nlp\nfrom nlp.main import app\n")

        replace_module_references(dest, "nlp", "my_app")

        content = (dest / "tests" / "test_main.py").read_text()
        assert "import my_app" in content
        assert "from my_app.main import app" in content


class TestGitInit:
    def test_git_init_does_not_change_cwd(self, tmp_path):
        runner = CliRunner()
        cwd_before = os.getcwd()

        result = runner.invoke(main, ["cwd_app", "-o", str(tmp_path)], catch_exceptions=False)

        assert result.exit_code == 0
        assert os.getcwd() == cwd_before
        assert (tmp_path / "cwd_app" / ".git").exists()

    def test_git_init_failure_prints_warning(self, tmp_path, monkeypatch):
        def failing_run(*args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=128, stdout=b"", stderr=b"fatal: boom")

        monkeypatch.setattr("cli.__main__.subprocess.run", failing_run)
        runner = CliRunner()

        result = runner.invoke(main, ["warn_app", "-o", str(tmp_path)], catch_exceptions=False)

        assert result.exit_code == 0
        assert "git init failed" in result.output


class TestCliFlags:
    def test_no_git_skips_git_init(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(main, ["test_app", "--no-git", "-o", str(tmp_path)], catch_exceptions=False)

        assert result.exit_code == 0
        assert not (tmp_path / "test_app" / ".git").exists()

    def test_output_dir(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(main, ["test_app", "-o", str(tmp_path)], catch_exceptions=False)

        assert result.exit_code == 0
        assert (tmp_path / "test_app").exists()
        assert (tmp_path / "test_app" / "pyproject.toml").exists()

    def test_output_dir_with_no_git(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(main, ["test_app", "-o", str(tmp_path), "--no-git"], catch_exceptions=False)

        assert result.exit_code == 0
        dest = tmp_path / "test_app"
        assert dest.exists()
        assert not (dest / ".git").exists()
