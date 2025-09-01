# SerpApi Job Finder CLI

[![CI](https://github.com/ryanmurphy-hub/serpapi-job-finder-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/ryanmurphy-hub/serpapi-job-finder-cli/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/badge/linting-ruff-blueviolet)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

A small CLI for searching Google Jobs via [SerpApi](https://serpapi.com).



# SerpApi Job Finder CLI

A small CLI for searching Google Jobs via [SerpApi](https://serpapi.com).

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e . requests python-dotenv
Copy-Item .env.example .env
# edit .env with your SERPAPI_API_KEY
python -m job_finder.cli --title "customer success engineer" --location "United States" --remote --limit 10
```

## Tests
```powershell
pytest
```

## CI
- Ruff lint (auto-fix) + matrix tests on Ubuntu/Windows/macOS (py310/py311).
- No live API calls in CI; tests are mocked.
