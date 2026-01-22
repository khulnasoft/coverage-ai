# UV Migration Guide

This guide covers migrating from Poetry to UV for the cover-agent project.

## Overview

UV is a modern, ultra-fast Python package installer that provides significant performance improvements over Poetry.

## Migration Steps

### 1. Update pyproject.toml

The build system has been updated from Poetry to Hatchling with UV support:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
# UV-specific configuration for optimized dependency management
dev-dependencies = [
    "pytest>=8.4.2",
    "pytest-cov>=7.0.0",
    "pytest-asyncio>=0.23.8",
    "pytest-timeout>=2.3.1",
    "fastapi>=0.111.1",
]
```

### 2. Update Development Commands

Replace Poetry commands with UV equivalents:

| Poetry Command | UV Command | Description |
|---------------|------------|-------------|
| `poetry install` | `uv sync` | Install dependencies |
| `poetry run pytest` | `uv run pytest` | Run tests |
| `poetry run` | `uv run` | Run any command |
| `poetry build` | `uv build` | Build package |

### 3. Update CI/CD Workflows

GitHub Actions workflows updated to use UV:

- **Setup**: Uses `astral-sh/setup-uv@v3` action
- **Caching**: Caches `~/.cache/uv` instead of Poetry cache
- **Installation**: `uv sync --dev` and `uv pip install -e .`
- **Testing**: `uv run pytest` instead of `poetry run pytest`

### 4. Update Documentation

All usage examples updated to show UV commands instead of Poetry.

## Benefits

- **10-100x faster** dependency resolution
- **Better caching** with UV's optimized cache
- **Simpler dependency management** with fewer lock conflicts
- **Better cross-platform compatibility**

## Verification

Test the migration:

```bash
# Install UV
pip install uv

# Test UV commands
uv sync --dev
uv run pytest --cov=coverage_ai --cov-report=xml
```

## Rollback Plan

If issues arise, rollback by:

1. Reverting `[build-system]` to Poetry:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

2. Restoring Poetry commands in workflows
3. Removing `[tool.uv]` section

## Support

For migration issues, check:
- UV documentation: https://docs.astral.sh/uv/
- Project issues: https://github.com/astral-sh/uv/issues
