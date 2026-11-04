"""Example usage of the Numu Tech Validation and Rollback module"""

from numu_tech.validation.rollback import (
    MigrationValidator,
    RollbackLog,
    ValidationStatus,
)

async def demo_validation_and_rollback():
    """Demonstrate validation and rollback workflow"""
    
    # Initialize validator
    validator = MigrationValidator()
    
    # Define validation checks for a migration
    validation_checks = [
        {"name": "database_schema_check", "type": "schema", "expected_pass": True},
        {"name": "api_endpoint_check", "type": "api", "expected_pass": True},
        {"name": "data_integrity_check", "type": "data", "expected_pass": True},
    ]
    
    # Run validation checks
    print("Running migration validation...")
    results = await validator.validate_migration("migration-001", validation_checks)
    
    # Display results
    print("\nValidation Results:")
    for result in results:
        status_icon = "[PASS]" if result.status == ValidationStatus.PASSED else "[FAIL]"
        print(f"  {status_icon} {result.check_name}: {result.message}")
    
    # Check if all passed
    all_passed = validator.all_validations_passed("migration-001")
    print(f"\nAll validations passed: {all_passed}")
    
    # Simulate rollback scenario
    print("\n--- Simulating Rollback Scenario ---")
    
    # Update some checks to fail to trigger rollback
    failed_checks = [
        {"name": "database_schema_check", "type": "schema", "expected_pass": True},
        {"name": "api_endpoint_check", "type": "api", "expected_pass": False},
        {"name": "data_integrity_check", "type": "data", "expected_pass": True},
    ]
    
    results = await validator.validate_migration("migration-002", failed_checks)
    
    print("\nValidation Results with Failure:")
    for result in results:
        status_icon = "[PASS]" if result.status == ValidationStatus.PASSED else "[FAIL]"
        print(f"  {status_icon} {result.check_name}: {result.message}")
    
    # Check if all passed
    all_passed = validator.all_validations_passed("migration-002")
    print(f"\nAll validations passed: {all_passed}")
    
    if not all_passed:
        print("\nInitiating rollback...")
        rollback_logs = await validator.rollback_migration(
            "migration-002",
            source="production-db",
            target="pre-migration-db",
            actions=[
            {
                "name": "schema_rollback",
                "target_resource": "database_schema",
                "expected_success": True,
            },
            {
                "name": "api_rollback",
                "target_resource": "api_endpoints",
                "expected_success": True,
            },
            {
                "name": "data_rollback",
                "target_resource": "data_integrity",
                "expected_success": True,
            },
            ]
        )
        
        print("\nRollback Logs:")
        for log_entry in rollback_logs:
            success_icon = "[SUCCESS]" if log_entry.success else "[FAILED]"
            print(f"  {success_icon} {log_entry.action}: {log_entry.success}")
    
    print("\n--- Demo Complete ---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_validation_and_rollback())