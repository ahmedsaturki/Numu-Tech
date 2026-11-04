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

## Development

```bash
# Run tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/prospects/test_cli.py

# Auto-format
black .

# Lint
ruff check .
```

## Architecture

- **Zero external dependencies** — Only Python standard library
- **Local storage** — JSON/CSV files only, no databases or APIs
- **Type-safe** — Full type hints with `dataclasses`
- **CLI-first** — Built with `argparse`, exit codes follow Unix conventions
- **Safe imports** — No re-exports in `numu_tech/__init__.py`

## License

MIT