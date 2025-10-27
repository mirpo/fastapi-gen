# Homebrew Release Setup

This document explains how the Homebrew release automation works for `fastapi-gen`.

## Overview

The Homebrew release workflow automatically publishes new versions of `fastapi-gen` to a Homebrew tap when a new version tag is pushed.

## Prerequisites

### 1. Create a Homebrew Tap Repository

You need to create a separate GitHub repository for your Homebrew tap:

- **Repository name**: `homebrew-fastapi-gen`
- **Full path**: `mirpo/homebrew-fastapi-gen`
- **Structure**: The repository should have a `Formula/` directory where the formula will be stored

To create the tap repository:

```bash
# Create a new repository on GitHub named 'homebrew-fastapi-gen'
# Then initialize it:
mkdir homebrew-fastapi-gen
cd homebrew-fastapi-gen
mkdir Formula
git init
git add Formula
git commit -m "Initial commit"
git remote add origin https://github.com/mirpo/homebrew-fastapi-gen.git
git push -u origin main
```

### 2. Set Up GitHub Token

The workflow requires a GitHub Personal Access Token with repository write permissions:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Homebrew Releaser")
4. Select scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
5. Generate the token and copy it
6. Add the token as a repository secret:
   - Go to your `fastapi-gen` repository
   - Settings → Secrets and variables → Actions
   - Add new repository secret named `HOMEBREW_GITHUB_API_TOKEN`
   - Paste the token value

## How It Works

### Workflow Trigger

The workflow (`.github/workflows/homebrew-release.yml`) triggers automatically when you push a version tag:

```bash
git tag v1.2.3
git push origin v1.2.3
```

### What Happens Automatically

1. **Formula Generation**: Creates/updates a Ruby formula file in `mirpo/homebrew-fastapi-gen/Formula/fastapi-gen.rb`
2. **Version Update**: Updates the version number in the formula
3. **Checksum Calculation**: Computes and updates the SHA256 checksum of the release tarball
4. **Python Resources**: Automatically discovers and adds all Python dependencies as Homebrew resources
5. **Commit & Push**: Commits the updated formula to the tap repository

### Formula Features

The generated formula includes:

- **Python virtualenv installation**: Installs the tool in an isolated Python environment
- **Automatic dependency management**: All PyPI dependencies are included as resources
- **Version pinning**: Dependencies are pinned to specific versions for reproducibility
- **Test command**: Includes a basic test to verify the installation (`fastapi-gen --version`)

## Installation for Users

Once published, users can install via:

```bash
brew tap mirpo/fastapi-gen
brew install fastapi-gen
```

Or in one command:

```bash
brew install mirpo/fastapi-gen/fastapi-gen
```

## Updating the Formula

The formula is automatically updated on each new release. You don't need to manually update it.

## Troubleshooting

### Workflow Fails: Repository Not Found

- Ensure `mirpo/homebrew-fastapi-gen` repository exists
- Verify the `HOMEBREW_GITHUB_API_TOKEN` secret has the correct permissions

### Formula Generation Fails

- Check that the release tarball is accessible
- Verify that `pyproject.toml` has correct dependencies listed
- Ensure the CLI entry point (`fastapi-gen`) is correctly defined in `pyproject.toml`

### Python Resources Not Updated

- The `update_python_resources` option only works with public repositories
- Ensure your repository is public, or you'll need to update resources manually

## Manual Formula Updates

If you need to manually update the formula:

```bash
# Clone the tap
git clone https://github.com/mirpo/homebrew-fastapi-gen.git
cd homebrew-fastapi-gen

# Edit the formula
vim Formula/fastapi-gen.rb

# Test locally
brew install --build-from-source ./Formula/fastapi-gen.rb
brew test fastapi-gen
brew audit --strict fastapi-gen

# Push changes
git add Formula/fastapi-gen.rb
git commit -m "Update fastapi-gen formula"
git push
```

## Resources

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Python for Formula Authors](https://docs.brew.sh/Python-for-Formula-Authors)
- [Homebrew Releaser Action](https://github.com/Justintime50/homebrew-releaser)
