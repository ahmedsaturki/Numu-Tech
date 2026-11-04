"""Tests for Prospect models."""
from datetime import datetime

from numu_tech.prospects.models import Prospect, ProspectStatus


def test_prospect_creation():
    """Test basic prospect creation."""
    prospect = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="Riyadh",
        status=ProspectStatus.NEW,
    )
    assert prospect.company_name == "Test Corp"
    assert prospect.industry == "Tech"
    assert prospect.city == "Riyadh"
    assert prospect.status == ProspectStatus.NEW
    assert prospect.prospect_id is not None
    assert isinstance(prospect.date_added, datetime)


def test_prospect_serialization():
    """Test prospect to_dict serialization."""
    prospect = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="Riyadh",
        status=ProspectStatus.NEW,
    )
    dict_repr = prospect.to_dict()
    assert dict_repr["company_name"] == "Test Corp"
    assert dict_repr["industry"] == "Tech"
    assert dict_repr["city"] == "Riyadh"
    assert dict_repr["status"] == "new"
    assert "prospect_id" in dict_repr
    assert "date_added" in dict_repr


def test_prospect_deserialization():
    """Test prospect from_dict deserialization."""
    dict_repr = {
        "company_name": "Test Corp",
        "industry": "Tech",
        "city": "Riyadh",
        "status": "new",
    }
    prospect = Prospect.from_dict(dict_repr)
    assert prospect.company_name == "Test Corp"
    assert prospect.industry == "Tech"
    assert prospect.city == "Riyadh"
    assert prospect.status == ProspectStatus.NEW


def test_prospect_status_enum():
    """Test ProspectStatus enum values."""
    assert ProspectStatus.NEW.value == "new"
    assert ProspectStatus.CONTACTED.value == "contacted"
    assert ProspectStatus.QUALIFIED.value == "qualified"
    assert ProspectStatus.NOT_INTERESTED.value == "not_interested"
    assert ProspectStatus.CONVERTED.value == "converted"
    assert ProspectStatus.DUPLICATE.value == "duplicate"


def test_invalid_status_handling():
    """Test that invalid status raises ValueError."""
    try:
        Prospect(
            company_name="Invalid Corp",
            industry="Tech",
            city="Riyadh",
            status="invalid",  # type: ignore
        )
        assert False, "Expected ValueError"
    except ValueError:
        pass  # Expected


def test_duplicate_detection():
    """Test duplicate detection rule."""
    prospect1 = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="Riyadh",
    )
    prospect2 = Prospect(
        company_name="test corp",  # Different case
        industry="Different",
        city="riyadh",  # Different case
    )
    prospect3 = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="Jeddah",  # Different city
    )
    
    assert prospect1.matches_duplicate_rule(prospect2)
    assert not prospect1.matches_duplicate_rule(prospect3)


def test_prospect_str():
    """Test prospect string representation."""
    prospect = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="Riyadh",
        status=ProspectStatus.NEW,
    )
    assert str(prospect) == "Test Corp (Riyadh) - new"