"""Integration tests for the validation and rollback demo workflow"""

import subprocess
import sys
from pathlib import Path

import pytest

from numu_tech.validation.rollback import (
    MigrationValidator,
    ValidationStatus,
)


class TestDemoIntegration:
    """Integration tests for the validation and rollback demo workflow."""

    @pytest.fixture(scope="module")
    def demo_script_path(self):
        """Return the path to the demo script."""
        return Path(__file__).parent.parent / "examples" / "validation_rollback_demo.py"

    @pytest.mark.asyncio
    async def test_demo_runs_end_to_end(self, demo_script_path):
        """Test that the demo script runs without exceptions and completes rollback flow."""
        result = subprocess.run(
            [sys.executable, str(demo_script_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert (
            result.returncode == 0
        ), f"Demo failed with exit code {result.returncode}\nSTDERR: {result.stderr}"
        assert "Demo Complete" in result.stdout, "Demo did not complete"
        assert "Initiating rollback" in result.stdout, "Rollback was not triggered"

    @pytest.mark.asyncio
    async def test_demo_with_real_config(self, demo_script_path):
        """Test demo with actual MigrationConfig from package."""
        result = subprocess.run(
            [sys.executable, str(demo_script_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert result.returncode == 0
        assert "Demo Complete" in result.stdout
        assert "Rollback Logs" in result.stdout

    @pytest.mark.asyncio
    async def test_import_and_usage_flow(self):
        """Test that MigrationValidator is importable and usable in validation flow."""
        validator = MigrationValidator()

        # Test validation
        checks = [{"name": "test", "type": "schema", "expected_pass": True}]
        results = await validator.validate_migration("test-migration", checks)
        assert len(results) == 1
        assert results[0].status == ValidationStatus.PASSED

    @pytest.mark.asyncio
    async def test_rollback_flow_success(self):
        """Test rollback flow with successful actions."""
        validator = MigrationValidator()

        checks = [{"name": "test", "type": "schema", "expected_pass": True}]
        await validator.validate_migration("test-migration", checks)

        rollback_logs = await validator.rollback_migration(
            "test-migration",
            source="prod",
            target="pre",
            actions=[{"name": "test", "target_resource": "resource", "expected_success": True}],
        )
        assert len(rollback_logs) > 0
        assert any(log.success for log in rollback_logs)

    @pytest.mark.asyncio
    async def test_rollback_flow_partial_failure(self):
        """Test rollback flow with partial failures."""
        validator = MigrationValidator()

        checks = [{"name": "test", "type": "schema", "expected_pass": False}]
        await validator.validate_migration("test-migration", checks)

        rollback_logs = await validator.rollback_migration(
            "test-migration",
            source="prod",
            target="pre",
            actions=[
                {
                    "name": "success_action",
                    "target_resource": "resource1",
                    "expected_success": True,
                },
                {
                    "name": "failed_action",
                    "target_resource": "resource2",
                    "expected_success": False,
                },
            ],
        )
        assert len(rollback_logs) == 2
        assert any(log.success for log in rollback_logs)
        assert any(not log.success for log in rollback_logs)
