# Numu Tech Prospects CLI

A local-only CLI tool for managing Riyadh-based contracting company prospects. Zero external dependencies, using JSON/CSV storage.

## Installation

```bash
# Clone and install
git clone <repo-url>
cd Numu-Tech
pip install -e .
```

## Usage

### Add a prospect

```bash
python -m numu_tech.prospects.__main__ add --file prospects.json "Company Name" "Industry" "Riyadh"
```

With optional fields:

```bash
python -m numu_tech.prospects.__main__ add --file prospects.json "Company" "Construction" "Riyadh" \
    --website "https://company.com" \
    --contact "John Doe" \
    --notes "High-value opportunity"
```

### List all prospects

```bash
python -m numu_tech.prospects.__main__ list --file prospects.json
```

### Check for duplicates

```bash
python -m numu_tech.prospects.__main__ check --file prospects.json
```

Returns exit code `1` if duplicates found, `0` if clean.

### Import from CSV

```bash
python -m numu_tech.prospects.__main__ import --file prospects.json --csv new_prospects.csv
```

CSV format:
```
company_name,industry,city,website,contact_name,status
Acme Corp,Construction,Riyadh,https://acme.com,John Smith,new
```

### Export to JSON

```bash
python -m numu_tech.prospects.__main__ export --file prospects.json --output backup.json
```

## Data Format

Prospects are stored as JSON array:

```json
[
  {
    "prospect_id": "a1b2c3d4",
    "company_name": "Acme Corp",
    "industry": "Construction",
    "city": "Riyadh",
    "website": "https://acme.com",
    "contact_name": "John Smith",
    "status": "new",
    "notes": "High-value opportunity",
    "created_at": "2026-11-04T14:10:00Z",
    "updated_at": "2026-11-04T14:10:00Z"
  }
]
```

## Status Values

- `new` — Recently added, no contact
- `contacted` — Initial contact made
- `qualified` — Meets criteria, pursuing
- `proposal` — Proposal sent
- `won` — Contract secured
- `lost` — Deal not secured
- `archived` — Inactive

## CI/CD

GitHub Actions pipeline runs on every push and pull request:

- **Lint job** — Runs ruff, black, and mypy on Python 3.12
- **Test job** — Runs pytest on Python 3.10, 3.11, and 3.12
- **Build job** — Creates distribution packages on main branch pushes

## Development

```bash
# Pre-commit hooks (recommended)
pre-commit install
pre-commit run --all-files

# Run tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/prospects/test_cli.py

# Type checking
mypy src/numu_tech

# Auto-format
black .

# Lint
ruff check .
```

## Architecture

### Migration Engine (`numu_tech.core`)

- **Core orchestration** — `MigrationEngine` manages multi-cloud migrations with security-hardened step dispatch
- **Explicit allowlist** — `STEP_METHODS` class variable prevents arbitrary `getattr` calls
- **Timezone-aware timestamps** — Uses `datetime.now(timezone.utc)` instead of deprecated `utcnow()`
- **Rollback orchestration** — Automatic rollback on failure with `create_rollback_plan()` adapter method

### Prospects CLI (`numu_tech.prospects`)

- **Zero external dependencies** — Only Python standard library
- **Local storage** — JSON/CSV files only, no databases or APIs
- **Type-safe** — Full type hints with `dataclasses`
- **CLI-first** — Built with `argparse`, exit codes follow Unix conventions

## Release Workflow

```bash
# Update version in pyproject.toml and src/numu_tech/__init__.py
# Update CHANGELOG.md with new version section
# Create PR and merge to main

# Tag the release
git fetch --tags
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

## License

MIT