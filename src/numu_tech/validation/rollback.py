"""Validation and rollback support for migrations"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime


class ValidationStatus(Enum):
    """Validation status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class ValidationResult:
    """Result of a validation check"""
    check_name: str
    status: ValidationStatus
    message: str
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RollbackLog:
    """Log entry for rollback operations"""
    action: str
    target_resource: str
    source_resource: str
    timestamp: str
    success: bool
    error_message: str = ""


class MigrationValidator:
    """Validates migration state and provides rollback support"""
    
    def __init__(self):
        self._validation_results: Dict[str, List[ValidationResult]] = {}
        self._rollback_logs: Dict[str, List[RollbackLog]] = {}
    
    async def validate_migration(
        self,
        plan_id: str,
        validation_checks: List[Dict[str, Any]]
    ) -> List[ValidationResult]:
        """Run validation checks on a migration"""
        results: List[ValidationResult] = []
        
        for check in validation_checks:
            result = await self._run_validation_check(plan_id, check)
            results.append(result)
        
        self._validation_results[plan_id] = results
        return results
    
    async def _run_validation_check(
        self,
        plan_id: str,
        check: Dict[str, Any]
    ) -> ValidationResult:
        """Run a single validation check"""
        check_name = check.get("name", "unknown")
        check_type = check.get("type", "generic")
        
        # Simulate validation check
        try:
            # Simulate async validation
            await asyncio.sleep(0.1)
            
            # Check if validation passes (simulated)
            is_passed = check.get("expected_pass", True)
            
            if is_passed:
                status = ValidationStatus.PASSED
                message = f"Validation check '{check_name}' passed"
            else:
                status = ValidationStatus.FAILED
                message = f"Validation check '{check_name}' failed"
            
            return ValidationResult(
                check_name=check_name,
                status=status,
                message=message,
                timestamp=str(datetime.now()),
                details={"type": check_type}
            )
        except Exception as e:
            return ValidationResult(
                check_name=check_name,
                status=ValidationStatus.FAILED,
                message=f"Validation error: {str(e)}",
                timestamp=str(datetime.now())
            )
    
    def get_validation_results(self, plan_id: str) -> List[ValidationResult]:
        """Get validation results for a plan"""
        return self._validation_results.get(plan_id, [])
    
    def all_validations_passed(self, plan_id: str) -> bool:
        """Check if all validations have passed"""
        results = self.get_validation_results(plan_id)
        return all(r.status == ValidationStatus.PASSED for r in results)
    
    async def rollback_migration(
        self,
        plan_id: str,
        source: Any,
        target: Any,
        actions: List[Dict[str, Any]]
    ) -> List[RollbackLog]:
        """Perform rollback operations for a failed migration"""
        log_entries: List[RollbackLog] = []
        
        for action in actions:
            log_entry = await self._execute_rollback_action(
                plan_id,
                action,
                source,
                target
            )
            log_entries.append(log_entry)
        
        self._rollback_logs[plan_id] = log_entries
        return log_entries
    
    async def _execute_rollback_action(
        self,
        plan_id: str,
        action: Dict[str, Any],
        source: Any,
        target: Any
    ) -> RollbackLog:
        """Execute a single rollback action"""
        action_name = action.get("name", "unknown")
        target_resource = action.get("target_resource", "unknown")
        
        try:
            # Simulate rollback action
            await asyncio.sleep(0.1)
            
            # Simulate success/failure
            success = action.get("expected_success", True)
            
            if success:
                return RollbackLog(
                    action=action_name,
                    target_resource=target_resource,
                    source_resource=str(source),
                    timestamp=str(datetime.now()),
                    success=True
                )
            else:
                return RollbackLog(
                    action=action_name,
                    target_resource=target_resource,
                    source_resource=str(source),
                    timestamp=str(datetime.now()),
                    success=False,
                    error_message="Rollback action failed"
                )
        except Exception as e:
            return RollbackLog(
                action=action_name,
                target_resource=target_resource,
                source_resource=str(source),
                timestamp=str(datetime.now()),
                success=False,
                error_message=str(e)
            )
    
    def get_rollback_log(self, plan_id: str) -> List[RollbackLog]:
        """Get rollback log for a plan"""
        return self._rollback_logs.get(plan_id, [])