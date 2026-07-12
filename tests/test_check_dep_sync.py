import textwrap

import pytest

from scripts.check_dep_sync import check_drift, collect_deps


@pytest.fixture
def tmp_project(tmp_path):
    def _write(rel_path: str, content: str):
        p = tmp_path / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(content))

    return _write, tmp_path


class TestCollectDeps:
    def test_extracts_pinned_project_dependencies(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1", "click==8.3.0"]
            """,
        )

        deps = collect_deps(root / "pyproject.toml")

        assert deps == {"fastapi": "0.136.1", "click": "8.3.0"}

    def test_extracts_dev_dependency_groups(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = []

            [dependency-groups]
            dev = ["ruff==0.15.13", "pytest==9.0.3"]
            """,
        )

        deps = collect_deps(root / "pyproject.toml")

        assert deps == {"ruff": "0.15.13", "pytest": "9.0.3"}

    def test_ignores_unpinned_dependencies(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi>=0.100", "uvicorn==0.47.0"]
            """,
        )

        deps = collect_deps(root / "pyproject.toml")

        assert deps == {"uvicorn": "0.47.0"}

    def test_normalizes_package_names(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["python-dotenv==1.2.2", "pydantic-settings==2.14.1"]
            """,
        )

        deps = collect_deps(root / "pyproject.toml")

        assert deps == {"python_dotenv": "1.2.2", "pydantic_settings": "2.14.1"}

    def test_strips_extras_from_name(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["uvicorn[standard]==0.47.0", "transformers[torch]==5.0.0"]
            """,
        )

        deps = collect_deps(root / "pyproject.toml")

        assert deps == {"uvicorn": "0.47.0", "transformers": "5.0.0"}

    def test_handles_no_project_section(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [build-system]
            requires = ["hatchling"]
            """,
        )

        deps = collect_deps(root / "pyproject.toml")

        assert deps == {}


class TestCheckDrift:
    def test_no_drift_when_versions_match(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            [dependency-groups]
            dev = ["ruff==0.15.13"]
            """,
        )
        write(
            "packages/template-a/pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            [dependency-groups]
            dev = ["ruff==0.15.13"]
            """,
        )
        write(
            "packages/template-b/pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            [dependency-groups]
            dev = ["ruff==0.15.13"]
            """,
        )

        drifted = check_drift(root)

        assert drifted == []

    def test_ignores_deps_appearing_in_single_file(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["click==8.3.3"]
            """,
        )
        write(
            "packages/template-a/pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            """,
        )

        drifted = check_drift(root)

        assert drifted == []

    def test_drift_returns_all_sources_and_versions(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.130.0"]
            """,
        )
        write(
            "packages/template-a/pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            """,
        )
        write(
            "packages/template-b/pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            """,
        )

        drifted = check_drift(root)

        assert len(drifted) == 1
        pkg, versions = drifted[0]
        assert pkg == "fastapi"
        assert versions["root"] == "0.130.0"
        assert versions["template-a"] == "0.136.1"
        assert versions["template-b"] == "0.136.1"

    def test_multiple_drifted_packages(self, tmp_project):
        write, root = tmp_project
        write(
            "pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.130.0"]
            [dependency-groups]
            dev = ["ruff==0.14.0"]
            """,
        )
        write(
            "packages/template-a/pyproject.toml",
            """\
            [project]
            dependencies = ["fastapi==0.136.1"]
            [dependency-groups]
            dev = ["ruff==0.15.13"]
            """,
        )

        drifted = check_drift(root)

        pkg_names = [d[0] for d in drifted]
        assert pkg_names == ["fastapi", "ruff"]

    def test_normalized_names_compared_correctly(self, tmp_project):
        write, root = tmp_project
        write(
            "packages/template-a/pyproject.toml",
            """\
            [project]
            dependencies = ["python-dotenv==1.2.2"]
            """,
        )
        write(
            "packages/template-b/pyproject.toml",
            """\
            [project]
            dependencies = ["python-dotenv==1.3.0"]
            """,
        )

        drifted = check_drift(root)

        assert len(drifted) == 1
        assert drifted[0][0] == "python_dotenv"
