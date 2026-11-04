"""Validation for prospect records."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Prospect, ProspectStatus


@dataclass
class ValidationReport:
    """Report of validation results for prospect records."""

    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Return True if all records are valid."""
        return self.invalid_records == 0

    def add_error(self, error: str) -> None:
        """Add an error to the report."""
        self.errors.append(error)

    def __str__(self) -> str:
        return (
            f"ValidationReport(total={self.total_records}, "
            f"valid={self.valid_records}, invalid={self.invalid_records})"
        )


def validate_record(prospect: Prospect) -> ValidationReport:
    """Validate a single prospect record.

    Returns a ValidationReport with errors if any.
    """
    report = ValidationReport(total_records=1)

    if not prospect.company_name or not prospect.company_name.strip():
        report.add_error("company_name is required")
    if not prospect.industry or not prospect.industry.strip():
        report.add_error("industry is required")
    if not prospect.city or not prospect.city.strip():
        report.add_error("city is required")
    if not isinstance(prospect.status, ProspectStatus):
        report.add_error(f"invalid status: {prospect.status}")

    if report.errors:
        report.invalid_records = 1
    else:
        report.valid_records = 1

    return report


def validate_records(prospects: list[Prospect]) -> ValidationReport:
    """Validate a list of prospect records."""
    report = ValidationReport(total_records=len(prospects))
    for i, prospect in enumerate(prospects):
        result = validate_record(prospect)
        if result.is_valid:
            report.valid_records += 1
        else:
            report.invalid_records += 1
            for error in result.errors:
                report.errors.append(f"Record {i}: {error}")
    return report