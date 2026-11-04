"""Tests for prospect storage operations."""
from pathlib import Path

from numu_tech.prospects.models import Prospect, ProspectStatus
from numu_tech.prospects.storage import (
    backup_file,
    import_from_csv,
    import_from_json,
    load_prospects,
    save_prospects,
)


def test_save_and_load_json(tmp_path: Path):
    """Test saving and loading prospects from JSON."""
    prospects = [
        Prospect(company_name="Test Corp", industry="Tech", city="Riyadh"),
        Prospect(company_name="Another Corp", industry="Construction", city="Jeddah"),
    ]
    json_file = tmp_path / "prospects.json"
    
    save_prospects(prospects, json_file)
    loaded = load_prospects(json_file)
    
    assert len(loaded) == 2
    assert loaded[0].company_name == "Test Corp"
    assert loaded[1].city == "Jeddah"


def test_load_nonexistent_file(tmp_path: Path):
    """Test loading from a nonexistent file returns empty list."""
    json_file = tmp_path / "nonexistent.json"
    loaded = load_prospects(json_file)
    assert loaded == []


def test_import_from_json(tmp_path: Path):
    """Test import_from_json alias."""
    prospects = [Prospect(company_name="Test Corp", industry="Tech", city="Riyadh")]
    json_file = tmp_path / "prospects.json"
    save_prospects(prospects, json_file)
    
    imported = import_from_json(json_file)
    assert len(imported) == 1
    assert imported[0].company_name == "Test Corp"


def test_import_from_csv(tmp_path: Path):
    """Test importing prospects from CSV."""
    csv_file = tmp_path / "prospects.csv"
    csv_content = """company_name,industry,city,website,contact_name,status
Test Corp,Tech,Riyadh,https://test.com,John Doe,new
Another Corp,Construction,Jeddah,,Jane Smith,contacted
"""
    csv_file.write_text(csv_content)
    
    imported = import_from_csv(csv_file)
    assert len(imported) == 2
    assert imported[0].company_name == "Test Corp"
    assert imported[0].website == "https://test.com"
    assert imported[0].contact_name == "John Doe"
    assert imported[0].status == ProspectStatus.NEW
    assert imported[1].status == ProspectStatus.CONTACTED


def test_import_from_nonexistent_csv(tmp_path: Path):
    """Test importing from nonexistent CSV returns empty list."""
    csv_file = tmp_path / "nonexistent.csv"
    imported = import_from_csv(csv_file)
    assert imported == []


def test_backup_file(tmp_path: Path):
    """Test creating a backup file."""
    original_file = tmp_path / "data.json"
    original_file.write_text('{"test": "data"}')
    
    backup_path = backup_file(original_file)
    assert backup_path.exists()
    assert backup_path.suffix == ".bak"
    assert backup_path.read_text() == '{"test": "data"}'


def test_backup_nonexistent_file(tmp_path: Path):
    """Test backup raises FileNotFoundError for nonexistent file."""
    nonexistent = tmp_path / "nonexistent.json"
    try:
        backup_file(nonexistent)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass  # Expected


def test_save_creates_parent_directories(tmp_path: Path):
    """Test that save_prospects creates parent directories."""
    nested_dir = tmp_path / "subdir" / "nested"
    json_file = nested_dir / "prospects.json"
    
    prospects = [Prospect(company_name="Test Corp", industry="Tech", city="Riyadh")]
    save_prospects(prospects, json_file)
    
    assert json_file.exists()
    assert nested_dir.exists()