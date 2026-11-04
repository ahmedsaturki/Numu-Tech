"""Core data structures for prospect management."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class ProspectStatus(str, Enum):
    """Status of a prospect record."""

    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    NOT_INTERESTED = "not_interested"
    CONVERTED = "converted"
    DUPLICATE = "duplicate"


class Prospect:
    """Prospect record representing a potential business contact."""

    def __init__(
        self,
        company_name: str,
        industry: str,
        city: str,
        prospect_id: str | None = None,
        website: str | None = None,
        business_contact_channel: str | None = None,
        contact_name: str | None = None,
        date_added: datetime | None = None,
        status: ProspectStatus = ProspectStatus.NEW,
        last_contact_date: datetime | None = None,
        next_action: str | None = None,
        notes: str | None = None,
    ):
        self.prospect_id = prospect_id or str(uuid4())
        self.company_name = company_name
        self.industry = industry
        self.city = city
        self.website = website
        self.business_contact_channel = business_contact_channel
        self.contact_name = contact_name
        self.date_added = date_added or datetime.now()
        if isinstance(status, str):
            status = ProspectStatus(status)
        self.status = status
        self.last_contact_date = last_contact_date
        self.next_action = next_action
        self.notes = notes or ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "prospect_id": self.prospect_id,
            "company_name": self.company_name,
            "industry": self.industry,
            "city": self.city,
            "website": self.website,
            "business_contact_channel": self.business_contact_channel,
            "contact_name": self.contact_name,
            "date_added": self.date_added.isoformat(),
            "status": self.status.value,
            "last_contact_date": self.last_contact_date.isoformat()
            if self.last_contact_date
            else None,
            "next_action": self.next_action,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Prospect:
        """Create from dictionary."""
        # Convert date strings back to datetime objects
        if isinstance(data.get("date_added"), str):
            data = {**data, "date_added": datetime.fromisoformat(data["date_added"])}
        if isinstance(data.get("last_contact_date"), str) and data.get(
            "last_contact_date"
        ):
            data = {
                **data,
                "last_contact_date": datetime.fromisoformat(data["last_contact_date"]),
            }

        # Convert status string to enum
        if isinstance(data.get("status"), str):
            data = {**data, "status": ProspectStatus(data["status"])}

        return cls(**data)

    def matches_duplicate_rule(self, other: Prospect) -> bool:
        """Check if this prospect matches the duplicate rule with another.

        Duplicate rule: same company name AND same city (case-insensitive).
        """
        return (
            self.company_name.lower().strip()
            == other.company_name.lower().strip()
            and self.city.lower().strip() == other.city.lower().strip()
        )

    def __str__(self) -> str:
        return f"{self.company_name} ({self.city}) - {self.status.value}"