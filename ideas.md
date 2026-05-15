# fastapi-gen: Improvement Ideas & Evaluation

## Current State Summary

- **5 templates** (hello_world, advanced, nlp, langchain, llama) as uv workspace members under `packages/`
- **1 CLI** (`src/cli/__main__.py`, 236 lines) — copies templates + string-replaces module names
- **~1,826 lines** of template application code across 5 `main.py` files
- **Already a monorepo** via `[tool.uv.workspace]` — templates are workspace members, single `uv.lock`
- **CI matrix**: 2 OS × 2 Python (3.11, 3.12), Renovate for deps, publish to PyPI on tag

---

## 1. Template Duplication — By Design

Each template generates a **standalone CLI project**. Users own the generated code — there's no runtime dependency on fastapi-gen. This means:

| Duplicated Artifact | Copies | Why It Must Be Duplicated |
|---|---|---|
| Makefile | 5 | Generated project needs its own build commands |
| pyproject.toml structure | 5 | Each project is independently installable/publishable |
| Ruff config | 5 | Generated project runs its own linting |
| Dev dependencies | 5 | Each project manages its own dev tooling |
| `/health` endpoint | 5 | Different response fields per domain |
| `.gitignore` | 5 | Generated project is its own git repo |

**This duplication is correct.** Extracting shared code into a library would defeat the purpose — generated projects must work without fastapi-gen installed.

### What we CAN do
Ensure the duplicated parts don't silently drift apart → see **#8 (Dependency Version Sync)**

---

## 2. Simplify the Build/Package Setup (Medium Impact)

### Problem
The `pyproject.toml` has a complex `[tool.hatch.build]` section that manually lists every template for both `include` and `force-include`. Adding a new template requires editing 4 places:
1. `[tool.hatch.build] include`
2. `[tool.hatch.build.targets.wheel.force-include]`
3. `[tool.uv.workspace] members`
4. `_template_map` in `__main__.py`

### Proposal: Auto-discovery
- **CLI**: Scan `packages/template-*/` at build time instead of hardcoded map. At runtime, discover templates from the installed package's `cli/templates/` directory.
- **pyproject.toml**: Use glob patterns where hatch supports them (or a hatch plugin for dynamic includes).
- **Benefit**: Adding a new template = just drop a directory in `packages/`. No config edits.

```python
# Instead of _template_map dict, discover at runtime:
def get_available_templates():
    templates_dir = get_templates_root()
    return {
        d.name.replace("template-", "").replace("-", "_"): d
        for d in templates_dir.iterdir() if d.is_dir()
    }
```

### Verdict: Worth doing — reduces friction for new templates from 4 edits to 0

---

## 3. Add CLI Unit Tests (High Impact)

### Problem
`src/cli/__main__.py` has **zero unit tests**. The only testing is integration (CI generates a project, runs `make test`). The Makefile literally says `"Phase 1: No root tests yet."` File renaming, import rewriting, and edge cases are untested.

### Proposal
- Test `is_valid_name()` with valid/invalid inputs
- Test `copy_template()` excludes dev artifacts
- Test `rename_package_in_pyproject()` correctly replaces names
- Test `update_imports_in_tests()` handles edge cases
- Test full generation end-to-end with a temp directory
- Add `make test` at root level that runs these

### Verdict: Essential — the core logic has no safety net

---

## 4. Monorepo? You Already Have One

### Current Structure
```
fastapi-gen/
├── src/cli/          # CLI package (root)
├── packages/
│   ├── template-hello-world/   # workspace member
│   ├── template-advanced/      # workspace member
│   ├── template-nlp/           # workspace member
│   ├── template-langchain/     # workspace member
│   └── template-llama/         # workspace member
├── pyproject.toml    # root + workspace config
└── uv.lock           # unified lockfile
```

This **is already a monorepo** via uv workspaces. The single `uv.lock` manages all deps. CI tests all templates in a matrix.

### What Could Be Better

| Aspect | Current | Improvement |
|---|---|---|
| Template discovery | Hardcoded in 4 places | Auto-discover from `packages/` |
| Shared dev tooling | Ruff config duplicated in each template | Templates use minimal config; root handles CI linting |
| Root tests | None | Add CLI unit tests |
| Template validation | CI only (generate + test) | Add pre-commit check that templates haven't drifted |

### Verdict: Monorepo is already in place — just tighten it

---

## 5. Simplify the Generation Engine (Medium Impact)

### Problem
The CLI does 6 sequential string-replace passes after copying:
1. `rename_package_in_pyproject`
2. `update_scripts_in_pyproject`
3. `rename_src_directory`
4. `update_imports_in_tests`
5. `update_makefile`
6. `update_readme`

Each function reads/writes the same files independently. Fragile if a template adds a new file that references the module name.

### Proposal A: Single-pass token replacement
Use a placeholder token (e.g., `__MODULE_NAME__`) in templates instead of the actual module name. One pass replaces all occurrences across all files.

**Pros**: Simpler, one function, handles any new file automatically.
**Cons**: Templates aren't directly runnable during development (need the placeholder replaced). This breaks the "templates are real projects" model that makes dev/test easy.

### Proposal B: Keep current approach, make it generic
Combine the 6 functions into one that takes a list of (glob, old, new) replacements. Less code, same behavior, no template changes.

```python
def replace_in_files(dest: Path, old_module: str, new_module: str):
    for path in dest.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".toml", ".md", ""}:
            content = path.read_text()
            updated = content.replace(f"{old_module}.", f"{new_module}.")
            updated = updated.replace(f"{old_module}/", f"{new_module}/")
            if updated != content:
                path.write_text(updated)
```

### Verdict: Proposal B — simpler code, templates stay runnable

---

## 6. Python Version Mess + Config Drift (Medium Impact)

### Problem: Python versions contradict each other across 4 sources

| Source | Python versions | Problem |
|---|---|---|
| `requires-python` (all pyproject.toml) | `>=3.11` | Claims 3.11+ support |
| CI test matrix (`test.yml`) | 3.11, 3.12 | Tests 3.11 but not 3.13 |
| Hatch envs matrix (root `pyproject.toml`) | 3.12, 3.13 | Doesn't list 3.11 |
| PyPI classifiers | 3.12, 3.13 | Tells PyPI "no 3.11 support" |
| Ruff target (root) | `py312` | Allows 3.12+ syntax in CLI |
| Ruff target (templates) | `py311` | Restricts templates to 3.11 syntax |
| Lint job in CI | `python-version: "3.11"` | Lints with 3.11 |

A user on 3.11 installs from PyPI, the classifiers say it's unsupported, but `requires-python` lets it install. Ruff in the root targets `py312`, so the CLI could use syntax that breaks on 3.11. Meanwhile CI *does* test 3.11 but *doesn't* test 3.13 despite classifiers advertising it.

### Proposal: Pick a truth and align everything

**Option A — Support 3.11+ (current `requires-python`):**
- Add `3.13` to CI matrix (since hatch/classifiers already claim it)
- Add `Programming Language :: Python :: 3.11` to classifiers
- Change root ruff `target-version` from `py312` → `py311`
- Change root hatch matrix from `["3.12", "3.13"]` → `["3.11", "3.12", "3.13"]`
- Keep template ruff at `py311` ✓

**Option B — Drop 3.11, support 3.12+:**
- Change `requires-python` to `>=3.12` everywhere
- Remove 3.11 from CI matrix
- Add 3.13 to CI matrix
- Root ruff `py312` is already correct ✓
- Change template ruff from `py311` → `py312`

### Verdict: Pick one and make all 4 sources agree. Either way, add 3.13 to CI — it's advertised but untested

---

## 7. Improve Template Extensibility (Future)

### Currently Missing
- No `--no-git` flag to skip git init
- No `--output-dir` flag to control destination
- No interactive mode (pick template from menu)
- No way to customize beyond project name (e.g., pick Python version, add/remove features)

### Proposal: Incremental CLI flags
Don't over-engineer. Add flags as needed:
1. `--no-git` — skip `git init` (useful for CI/testing)
2. `--output-dir` / `-o` — generate into a specific directory
3. Interactive template picker when no `--template` given (use `click.prompt` with choices)

### Verdict: Nice-to-have, low effort for `--no-git` and `-o`

---

## 8. Dependency Version Sync (Medium Impact) ← APPROVED FOR IMPLEMENTATION

### Problem
11 dependencies are shared across 2+ pyproject.toml files. Today they're in sync, but only because Renovate's grouping config has been catching them. One missed group = silent drift.

**Current shared deps (all aligned today):**
| Package | Appears in |
|---|---|
| `fastapi` | all 5 templates |
| `uvicorn` | all 5 templates |
| `pydantic-settings` | all 5 templates |
| `ruff` | root + all 5 templates |
| `pytest` | root + all 5 templates |
| `httpx` | all 5 templates |
| `pytest-asyncio` | advanced, langchain |
| `python-dotenv` | hello_world, advanced |
| `torch` | nlp, langchain |
| `transformers` | nlp, langchain |
| `accelerate` | nlp, langchain |

### Implementation Plan

**Step 1: Create `scripts/check_dep_sync.py`**

Script that:
1. Parses all `pyproject.toml` files (root + `packages/*/pyproject.toml`)
2. Extracts `[project].dependencies` and `[dependency-groups].dev`
3. Groups by package name (normalized: lowercase, hyphens → underscores)
4. Flags any package that appears in 2+ files with different pinned versions
5. Exits with code 1 on drift (CI-friendly)

```python
#!/usr/bin/env python3
"""Check that shared dependencies have consistent versions across all pyproject.toml files."""

import sys
import tomllib
from pathlib import Path

def parse_dep(dep_str: str) -> tuple[str, str]:
    """Extract (normalized_name, version_pin) from a dependency string."""
    # Handle extras: "transformers[torch]==5.0.0" → "transformers", "5.0.0"
    name = dep_str.split("[")[0].split("==")[0].split(">=")[0].split("<")[0].strip()
    normalized = name.lower().replace("-", "_")
    version = dep_str.split("==")[1] if "==" in dep_str else None
    return normalized, version

def collect_deps(pyproject_path: Path) -> dict[str, str]:
    """Collect all pinned deps from a pyproject.toml."""
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

def main():
    root = Path(__file__).parent.parent
    files = [root / "pyproject.toml"] + sorted(root.glob("packages/*/pyproject.toml"))
    
    # {package: {source_label: version}}
    all_deps: dict[str, dict[str, str]] = {}
    for f in files:
        label = f.parent.name if f.parent.name != root.name else "root"
        for pkg, ver in collect_deps(f).items():
            all_deps.setdefault(pkg, {})[label] = ver
    
    # Check for drift in shared deps
    drifted = []
    for pkg, versions in sorted(all_deps.items()):
        if len(versions) > 1 and len(set(versions.values())) > 1:
            drifted.append((pkg, versions))
    
    if drifted:
        print("DEPENDENCY VERSION DRIFT DETECTED:\n")
        for pkg, versions in drifted:
            print(f"  {pkg}:")
            for source, ver in sorted(versions.items()):
                print(f"    {source}: {ver}")
            print()
        sys.exit(1)
    
    shared = [(p, v) for p, v in all_deps.items() if len(v) > 1]
    print(f"OK — {len(shared)} shared dependencies, all versions aligned.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Step 2: Add to CI**

Add a step in `test.yml` lint-and-build job:

```yaml
- name: Check dependency version sync
  run: uv run python scripts/check_dep_sync.py
```

**Step 3: Add to root Makefile**

```makefile
check-deps:
	uv run python scripts/check_dep_sync.py
```

**Step 4: (Optional) Also check ruff config and dev tool versions**

Extend the script to also verify:
- `[tool.ruff].target-version` is consistent across templates
- `[tool.ruff].line-length` is consistent across templates
- `[tool.ruff.lint].select` is consistent across templates

### What this catches
- Renovate updates `fastapi` in 4 templates but misses the 5th
- Manual edit bumps `ruff` in root but not in templates
- New template copy-pasted from old one with stale versions

### What this does NOT replace
- Renovate still does the actual updating
- `uv.lock` still resolves the actual installed versions in the workspace
- This is a **consistency check**, not a dependency manager

---

## Priority Ranking

| # | Idea | Impact | Effort | Status |
|---|---|---|---|---|
| 8 | Dependency version sync check | Medium | Low | **→ DO NOW** |
| 6 | Python version alignment + CI 3.13 | Medium | Low | **→ DO NOW** (alongside #8) |
| 3 | CLI unit tests | High | Medium | Next |
| 2 | Auto-discovery (simplify adding templates) | Medium | Medium | Next |
| 5B | Generic replacement function | Medium | Low | Next |
| 7 | CLI flags (`--no-git`, `-o`) | Low | Low | Nice-to-have |
| 1 | Template duplication | — | — | Resolved: intentional by design |

---

## What NOT To Do

- **Don't switch to Copier/Cookiecutter** — the current approach (real runnable projects + string replace) is simpler and means templates are testable as-is during development. Templating engines add complexity for minimal benefit at this scale.
- **Don't extract shared template code into a library** — generated projects must be standalone. Shared code creates a runtime dependency on fastapi-gen.
- **Don't restructure into a different monorepo tool** — uv workspaces already work well here. No need for Nx, Turborepo, or similar.
- **Don't add type checking (mypy) to templates** — keep generated projects approachable. Users can add mypy themselves.
