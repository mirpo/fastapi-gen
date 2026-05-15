import textwrap
from pathlib import Path

import pytest

from cli.__main__ import (
    copy_template,
    is_valid_name,
    rename_package_in_pyproject,
    update_imports_in_tests,
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
        ["my-app", "my.app", "my app", "", "hello/world", "app@2", "café"],
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


class TestUpdateImportsInTests:
    def test_replaces_from_imports(self, tmp_path):
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "test_main.py"
        test_file.write_text("from nlp.main import app\nfrom nlp.config import settings\n")

        update_imports_in_tests(tests_dir, "nlp", "my_app")

        content = test_file.read_text()
        assert "from my_app.main import app" in content
        assert "from my_app.config import settings" in content

    def test_replaces_bare_imports(self, tmp_path):
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "test_main.py"
        test_file.write_text("import nlp\n")

        update_imports_in_tests(tests_dir, "nlp", "my_app")

        assert "import my_app" in test_file.read_text()

    def test_skips_init_files(self, tmp_path):
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        init = tests_dir / "__init__.py"
        init.write_text("from nlp.main import app")

        update_imports_in_tests(tests_dir, "nlp", "my_app")

        assert "from nlp.main" in init.read_text()

    def test_does_not_overmatch_prefix(self, tmp_path):
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        test_file = tests_dir / "test_main.py"
        test_file.write_text("from nlp.main import app\nfrom nlp_utils import helper\n")

        update_imports_in_tests(tests_dir, "nlp", "my_app")

        content = test_file.read_text()
        assert "from my_app.main import app" in content
        assert "from nlp_utils import helper" in content
