"""Tests for CLI prospect management."""
import tempfile
from pathlib import Path

from numu_tech.prospects.cli import cmd_add, cmd_check, cmd_export, cmd_import, cmd_list


def test_cmd_add(tmp_path: Path):
    """Test adding a prospect via CLI."""
    json_file = tmp_path / "prospects.json"
    args = type("Args", (), {
        "file": str(json_file),
        "company": "Test Corp",
        "industry": "Tech",
        "city": "Riyadh",
        "website": None,
        "contact": None,
        "notes": None,
    })()
    
    result = cmd_add(args)
    assert result == 0
    assert json_file.exists()


def test_cmd_list(tmp_path: Path):
    """Test listing prospects via CLI."""
    json_file = tmp_path / "prospects.json"
    json_file.write_text("[]")
    
    args = type("Args", (), {"file": str(json_file)})()
    result = cmd_list(args)
    assert result == 0


def test_cmd_check(tmp_path: Path):
    """Test checking for duplicates via CLI."""
    json_file = tmp_path / "prospects.json"
    # Create a JSON file with some prospects
    json_content = """[
        {"prospect_id": "1", "company_name": "Test Corp", "industry": "Tech", "city": "Riyadh"},
        {"prospect_id": "2", "company_name": "Test Corp", "industry": "Tech", "city": "Riyadh"},
        {"prospect_id": "3", "company_name": "Different Corp", "industry": "Tech", "city": "Riyadh"}
    ]"""
    json_file.write_text(json_content)
    
    args = type("Args", (), {"file": str(json_file)})()
    result = cmd_check(args)
    assert result == 1  # Should detect duplicates


def test_cmd_export(tmp_path: Path):
    """Test exporting prospects via CLI."""
    json_file = tmp_path / "prospects.json"
    output_file = tmp_path / "output.json"
    
    # Create input file
    json_content = """[
        {"prospect_id": "1", "company_name": "Test Corp", "industry": "Tech", "city": "Riyadh"}
    ]"""
    json_file.write_text(json_content)
    
    args = type("Args", (), {"file": str(json_file), "output": str(output_file)})()
    result = cmd_export(args)
    assert result == 0
    assert output_file.exists()


def test_cmd_import(tmp_path: Path):
    """Test importing prospects via CLI."""
    json_file = tmp_path / "prospects.json"
    csv_file = tmp_path / "prospects.csv"
    
    # Create CSV content
    csv_content = """company_name,industry,city,website,contact_name,status
New Corp,Construction,Riyadh,https://newcorp.com,John Doe,new
Another Corp,Services,Jeddah,,Jane Smith,contacted"""
    csv_file.write_text(csv_content)
    
    # Initialize empty JSON file
    json_file.write_text("[]")
    
    args = type("Args", (), {"file": str(json_file), "csv_file": str(csv_file)})()
    result = cmd_import(args)
    assert result == 0
    
    # Verify prospects were imported
    data = json_file.read_text()
    assert "New Corp" in data
    assert "Another Corp" in data


def test_cmd_add_arguments(tmp_path: Path):
    """Test CLI add command with all optional arguments."""
    json_file = tmp_path / "prospects.json"
    args = type("Args", (), {
        "file": str(json_file),
        "company": "Complete Corp",
        "industry": "Services",
        "city": "Jeddah",
        "website": "https://complete.com",
        "contact": "Alice Smith",
        "notes": "Important prospect"
    })()
    
    result = cmd_add(args)
    assert result == 0
    assert json_file.exists()


def test_cmd_list_empty():
    """Test listing when no prospects exist."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("[]")
        json_file = f.name
    
    try:
        args = type("Args", (), {"file": json_file})()
        result = cmd_list(args)
        assert result == 0
    finally:
        Path(json_file).unlink()


def test_cmd_check_no_duplicates(tmp_path: Path):
    """Test check command when no duplicates exist."""
    json_file = tmp_path / "prospects.json"
    
    # Create JSON with non-duplicate prospects
    json_content = """[
        {"prospect_id": "1", "company_name": "Corp A", "industry": "Tech", "city": "Riyadh"},
        {"prospect_id": "2", "company_name": "Corp B", "industry": "Construction", "city": "Jeddah"}
    ]"""
    json_file.write_text(json_content)
    
    args = type("Args", (), {"file": str(json_file)})()
    result = cmd_check(args)
    assert result == 0  # Should return 0 (success) when no duplicates
