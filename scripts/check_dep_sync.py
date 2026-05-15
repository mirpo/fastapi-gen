import re
import sys
import tomllib
from pathlib import Path

_DEP_RE = re.compile(r"^([A-Za-z0-9_.-]+)(?:\[.*?\])?==(.+)$")


def parse_dep(dep_str: str) -> tuple[str, str | None]:
    m = _DEP_RE.match(dep_str.strip())
    if not m:
        return dep_str.split("[", maxsplit=1)[0].strip().lower().replace("-", "_"), None
    return m.group(1).lower().replace("-", "_"), m.group(2)


def collect_deps(pyproject_path: Path) -> dict[str, str]:
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    deps = {}
    for d in data.get("project", {}).get("dependencies", []):
        name, ver = parse_dep(d)
        if ver:
            deps[name] = ver
    for group in data.get("dependency-groups", {}).values():
        for d in group:
            if isinstance(d, str):
                name, ver = parse_dep(d)
                if ver:
                    deps[name] = ver
    return deps


def check_drift(root: Path) -> list[tuple[str, dict[str, str]]]:
    files = sorted(root.glob("packages/*/pyproject.toml"))
    root_pyproject = root / "pyproject.toml"
    if root_pyproject.exists():
        files.insert(0, root_pyproject)

    all_deps: dict[str, dict[str, str]] = {}
    for f in files:
        label = f.parent.name if f.parent != root else "root"
        for pkg, ver in collect_deps(f).items():
            all_deps.setdefault(pkg, {})[label] = ver

    return [
        (pkg, versions)
        for pkg, versions in sorted(all_deps.items())
        if len(versions) > 1 and len(set(versions.values())) > 1
    ]


def main():
    root = Path(__file__).parent.parent
    drifted = check_drift(root)

    if drifted:
        print("DEPENDENCY VERSION DRIFT DETECTED:\n")
        for pkg, versions in drifted:
            print(f"  {pkg}:")
            for source, ver in sorted(versions.items()):
                print(f"    {source}: {ver}")
            print()
        sys.exit(1)

    print("OK — all shared dependency versions aligned.")


if __name__ == "__main__":
    main()
