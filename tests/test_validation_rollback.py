"""Tests for migration validation and rollback workflow."""
import pytest

from numu_tech.validation.rollback import (
    MigrationValidator,
    RollbackLog,
    ValidationStatus,
)


class TestMigrationValidator:
    """Test suite for MigrationValidator"""

    @pytest.mark.asyncio
    async def test_all_checks_pass(self):
        """Test validation where all checks pass."""
        validator = MigrationValidator()
        checks = [
            {"name": "db_check", "type": "database", "expected_pass": True},
            {"name": "api_check", "type": "api", "expected_pass": True},
        ]
        results = await validator.validate_migration("mig-001", checks)

        assert len(results) == 2
        assert all(r.status == ValidationStatus.PASSED for r in results)
        assert validator.all_validations_passed("mig-001")

    @pytest.mark.asyncio
    async def test_some_checks_fail(self):
        """Test validation where some checks fail."""
        validator = MigrationValidator()
        checks = [
            {"name": "db_check", "type": "database", "expected_pass": True},
            {"name": "api_check", "type": "api", "expected_pass": False},
            {"name": "data_check", "type": "data", "expected_pass": True},
        ]
        results = await validator.validate_migration("mig-002", checks)

        assert len(results) == 3
        failed = [r for r in results if r.status == ValidationStatus.FAILED]
        passed = [r for r in results if r.status == ValidationStatus.PASSED]
        assert len(failed) == 1
        assert len(passed) == 2
        assert not validator.all_validations_passed("mig-002")

    @pytest.mark.asyncio
    async def test_all_checks_fail(self):
        """Test validation where all checks fail."""
        validator = MigrationValidator()
        checks = [
            {"name": "check1", "type": "test", "expected_pass": False},
            {"name": "check2", "type": "test", "expected_pass": False},
        ]
        results = await validator.validate_migration("mig-003", checks)

        assert all(r.status == ValidationStatus.FAILED for r in results)
        assert not validator.all_validations_passed("mig-003")

    @pytest.mark.asyncio
    async def test_rollback_success(self):
        """Test rollback where all actions succeed."""
        validator = MigrationValidator()
        # First run validation to register the migration
        checks = [{"name": "check1", "type": "test", "expected_pass": False}]
        await validator.validate_migration("mig-004", checks)

        actions = [
            {"name": "action1", "target_resource": "res1", "expected_success": True},
            {"name": "action2", "target_resource": "res2", "expected_success": True},
        ]
        logs = await validator.rollback_migration(
            "mig-004", source="src", target="tgt", actions=actions
        )

        assert len(logs) == 2
        assert all(log.success for log in logs)
        assert all(isinstance(log, RollbackLog) for log in logs)

    @pytest.mark.asyncio
    async def test_rollback_partial_failure(self):
        """Test rollback where some actions fail."""
        validator = MigrationValidator()
        checks = [{"name": "check1", "type": "test", "expected_pass": False}]
        await validator.validate_migration("mig-005", checks)

        actions = [
            {"name": "action1", "target_resource": "res1", "expected_success": True},
            {"name": "action2", "target_resource": "res2", "expected_success": False},
        ]
        logs = await validator.rollback_migration(
            "mig-005", source="src", target="tgt", actions=actions
        )

        assert len(logs) == 2
        successes = [log for log in logs if log.success]
        failures = [log for log in logs if not log.success]
        assert len(successes) == 1
        assert len(failures) == 1

    @pytest.mark.asyncio
    async def test_rollback_without_prior_validation(self):
        """Test rollback on a migration that was not validated."""
        validator = MigrationValidator()
        actions = [{"name": "action1", "target_resource": "res1", "expected_success": True}]

        # Should not raise, but return empty or error logs
        logs = await validator.rollback_migration(
            "nonexistent", source="src", target="tgt", actions=actions
        )
        # The validator handles this gracefully
        assert isinstance(logs, list)

    @pytest.mark.asyncio
    async def test_empty_validation_checks(self):
        """Test validation with no checks."""
        validator = MigrationValidator()
        results = await validator.validate_migration("mig-006", [])
        assert len(results) == 0
        # Empty checks should be considered passed
        assert validator.all_validations_passed("mig-006")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])