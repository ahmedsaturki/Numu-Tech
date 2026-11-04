"""Prospect data manager for Numu Tech.

Local-only tool for organizing prospective Riyadh companies.
No network access, no external services.
"""

from __future__ import annotations

from .cli import main
from .models import Prospect, ProspectStatus
from .storage import (
    backup_file,
    import_from_csv,
    import_from_json,
    load_prospects,
    save_prospects,
)
from .validator import (
    ValidationReport,
    validate_record,
    validate_records,
)

__all__ = [
    "Prospect",
    "ProspectStatus",
    "ValidationReport",
    "backup_file",
    "import_from_csv",
    "import_from_json",
    "load_prospects",
    "main",
    "save_prospects",
    "validate_record",
    "validate_records",
]