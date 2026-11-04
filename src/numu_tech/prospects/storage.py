"""JSON/CSV storage for prospect data."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Prospect


def load_prospects(path: str | Path) -> list[Prospect]:
    """Load prospects from a JSON file."""
    path = Path(path)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [Prospect.from_dict(item) for item in data]


def save_prospects(prospects: list[Prospect], path: str | Path) -> None:
    """Save prospects to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in prospects], f, indent=2, ensure_ascii=False)


def import_from_json(path: str | Path) -> list[Prospect]:
    """Import prospects from a JSON file (alias for load_prospects)."""
    return load_prospects(path)


def import_from_csv(path: str | Path) -> list[Prospect]:
    """Import prospects from a CSV file."""
    path = Path(path)
    if not path.exists():
        return []
    prospects: list[Prospect] = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map CSV columns to Prospect fields
            data = {
                "company_name": row.get("company_name", ""),
                "industry": row.get("industry", ""),
                "city": row.get("city", ""),
                "website": row.get("website") or None,
                "business_contact_channel": row.get("business_contact_channel") or None,
                "contact_name": row.get("contact_name") or None,
                "status": row.get("status", "new"),
                "next_action": row.get("next_action") or None,
                "notes": row.get("notes") or None,
            }
            prospects.append(Prospect.from_dict(data))
    return prospects


def backup_file(path: str | Path) -> Path:
    """Create a backup copy of a file and return the backup path."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    backup_path = path.with_suffix(path.suffix + ".bak")
    backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup_path