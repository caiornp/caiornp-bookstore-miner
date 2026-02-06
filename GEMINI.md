# Project: caiornp-bookstore-miner

## Overview
This is a Python project focused on mining data from bookstores.

## Branching Strategy (GitFlow for AI)
Strict separation between "working code" and "agent experiments":
- **main**: The "Gold Copy." This code always works. Read-only for agents.
- **develop**: The integration branch. Agents merge here first to check for conflicts.
- **agent/{agent-name}/{task-ID}**: The sandbox. Each agent gets its own branch to work in.

**The Rule**: Agents never commit to `main`. They must submit a Pull Request (PR).

## Guidelines
- **Coding Style**: Follow PEP 8. Use `ruff`, `flake8` for linting and `black`, `ruff` for formatting.
- **Typing**: Use static type hints throughout the codebase.
- **Testing**: Use `pytest` for all tests. Ensure tests are placed in the `tests/` directory.
- **Documentation**: Use Google-style docstrings.

## Common Commands
- **Install dependencies**: `pip install -r requirements.txt`
- **Run tests**: `pytest`
- **Lint**: `ruff check .` or `flake8 .`
- **Format**: `ruff format .` or `black .`

## Specific Rules
- Always use `pathlib` for file system operations.
- Prefer asynchronous requests (e.g., `httpx` or `aiohttp`) if mining from multiple sources.
- Ensure all scraped data is validated using `pydantic` models.
