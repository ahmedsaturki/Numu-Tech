"""Tests for prospect validation."""
from numu_tech.prospects.models import Prospect, ProspectStatus
from numu_tech.prospects.validator import ValidationReport, validate_record, validate_records


def test_validate_valid_record():
    """Test validation of a valid prospect."""
    prospect = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="Riyadh",
        status=ProspectStatus.NEW,
    )
    report = validate_record(prospect)
    
    assert report.is_valid
    assert report.valid_records == 1
    assert report.invalid_records == 0
    assert len(report.errors) == 0


def test_validate_missing_company_name():
    """Test validation fails when company_name is missing."""
    prospect = Prospect(
        company_name="",
        industry="Tech",
        city="Riyadh",
    )
    report = validate_record(prospect)
    
    assert not report.is_valid
    assert "company_name is required" in report.errors


def test_validate_missing_industry():
    """Test validation fails when industry is missing."""
    prospect = Prospect(
        company_name="Test Corp",
        industry="",
        city="Riyadh",
    )
    report = validate_record(prospect)
    
    assert not report.is_valid
    assert "industry is required" in report.errors


def test_validate_missing_city():
    """Test validation fails when city is missing."""
    prospect = Prospect(
        company_name="Test Corp",
        industry="Tech",
        city="",
    )
    report = validate_record(prospect)
    
    assert not report.is_valid
    assert "city is required" in report.errors


def test_validate_whitespace_only_fields():
    """Test validation fails for whitespace-only fields."""
    prospect = Prospect(
        company_name="  ",
        industry="Tech",
        city="Riyadh",
    )
    report = validate_record(prospect)
    
    assert not report.is_valid
    assert "company_name is required" in report.errors


def test_validate_multiple_errors():
    """Test validation captures multiple errors."""
    prospect = Prospect(
        company_name="",
        industry="",
        city="Riyadh",
    )
    report = validate_record(prospect)
    
    assert not report.is_valid
    assert "company_name is required" in report.errors
    assert "industry is required" in report.errors
    assert report.invalid_records == 1


def test_validate_records():
    """Test validation of multiple records."""
    prospects = [
        Prospect(company_name="Valid Corp", industry="Tech", city="Riyadh"),
        Prospect(company_name="", industry="Tech", city="Riyadh"),
        Prospect(company_name="Another Corp", industry="Construction", city="Jeddah"),
    ]
    report = validate_records(prospects)
    
    assert not report.is_valid
    assert report.total_records == 3
    assert report.valid_records == 2
    assert report.invalid_records == 1


def test_validation_report_str():
    """Test ValidationReport string representation."""
    report = ValidationReport(total_records=10, valid_records=8, invalid_records=2)
    assert str(report) == "ValidationReport(total=10, valid=8, invalid=2)"


def test_add_error():
    """Test adding errors to a report."""
    report = ValidationReport()
    report.add_error("First error")
    report.add_error("Second error")
    
    assert len(report.errors) == 2
    assert report.invalid_records == 0
    assert "First error" in report.errors
    assert "Second error" in report.errors