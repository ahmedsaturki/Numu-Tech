"""Core migration engine for Numu Tech"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, cast

from .adapters.base import CloudAdapter
from .mappers.dependency import DependencyMapper


def _utcnow_iso() -> str:
    """Get current UTC time in ISO format"""
    return datetime.utcnow().isoformat()


class MigrationStatus(Enum):
    """Status of a migration operation"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class MigrationTarget:
    """Represents a target cloud resource or service"""

    id: str
    name: str
    type: str  # e.g., "compute", "storage", "database", "network"
    provider: str  # e.g., "azure", "aws", "gcp"
    region: str
    config: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MigrationPlan:
    """A migration plan with steps and acceptance criteria"""

    id: str
    name: str
    source: MigrationTarget
    target: MigrationTarget
    steps: list[dict[str, Any]] = field(default_factory=list)
    acceptance_criteria: dict[str, Any] = field(default_factory=dict)
    rollback_plan: dict[str, Any] | None = None
    status: MigrationStatus = MigrationStatus.PENDING
    created_at: str = field(default_factory=_utcnow_iso)


@dataclass
class MigrationResult:
    """Result of a migration execution"""

    plan_id: str
    success: bool
    migrated_resources: list[str] = field(default_factory=list)
    failed_resources: list[str] = field(default_factory=list)
    rollback_performed: bool = False
    execution_time_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)


class MigrationEngine:
    """Core engine that orchestrates cloud migrations"""

    def __init__(self) -> None:
        self._adapters: dict[str, CloudAdapter] = {}
        self._plans: dict[str, MigrationPlan] = {}
        self._dependency_mapper = DependencyMapper()

    def register_adapter(self, provider: str, adapter: CloudAdapter) -> None:
        """Register a cloud provider adapter"""
        self._adapters[provider] = adapter

    def create_plan(
        self,
        plan_id: str,
        name: str,
        source: MigrationTarget,
        target: MigrationTarget,
        steps: list[dict[str, Any]] | None = None,
    ) -> MigrationPlan:
        """Create a new migration plan"""
        plan = MigrationPlan(
            id=plan_id,
            name=name,
            source=source,
            target=target,
            steps=steps or [],
        )
        self._plans[plan_id] = plan
        return plan

    def get_plan(self, plan_id: str) -> MigrationPlan | None:
        """Get a migration plan by ID"""
        return self._plans.get(plan_id)

    async def execute_plan(self, plan_id: str) -> MigrationResult:
        """Execute a migration plan"""
        plan = self.get_plan(plan_id)
        if not plan:
            raise ValueError(f"Plan {plan_id} not found")

        plan.status = MigrationStatus.IN_PROGRESS
        result = MigrationResult(plan_id=plan_id, success=False)

        try:
            for step in plan.steps:
                step_result = await self._execute_step(step, plan)
                result.migrated_resources.extend(step_result.get("migrated", []))
                result.failed_resources.extend(step_result.get("failed", []))

                if step_result.get("failed"):
                    break

            if not result.failed_resources:
                plan.status = MigrationStatus.COMPLETED
                result.success = True
            else:
                plan.status = MigrationStatus.FAILED
                # Execute rollback
                if plan.rollback_plan:
                    await self._execute_rollback(plan.rollback_plan)
                    result.rollback_performed = True

        except Exception as e:
            plan.status = MigrationStatus.FAILED
            result.errors.append(str(e))
            if plan.rollback_plan:
                await self._execute_rollback(plan.rollback_plan)
                result.rollback_performed = True

        result.execution_time_seconds = (
            datetime.utcnow() - datetime.fromisoformat(plan.created_at)
        ).total_seconds()

        return result

    async def _execute_step(self, step: dict[str, Any], plan: MigrationPlan) -> dict[str, Any]:
        """Execute a single migration step"""
        step_type = step.get("type", "generic")
        provider = step.get("provider", "azure")

        adapter = self._adapters.get(provider)
        if not adapter:
            return {"migrated": [], "failed": [f"No adapter for provider {provider}"]}

        method = getattr(adapter, step_type, None)
        if not method:
            return {"migrated": [], "failed": [f"Step type {step_type} not found on adapter"]}

        return cast("dict[str, Any]", await method(step.get("params", {})))

    async def _execute_rollback(self, rollback_plan: dict[str, Any]) -> None:
        """Execute rollback plan"""
        for step in rollback_plan.get("steps", []):
            provider = step.get("provider", "azure")
            adapter = self._adapters.get(provider)
            if adapter:
                method = getattr(adapter, step.get("type", "generic"), None)
                if method:
                    await method(step.get("params", {}))
