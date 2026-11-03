"""Migration planning engine"""

from datetime import datetime
from typing import Any

from numu_tech.core import MigrationPlan


class MigrationPlanner:
    """Plans and manages migration execution"""

    def __init__(self):
        self._plans: dict[str, MigrationPlan] = {}

    def create_plan(
        self,
        plan_id: str,
        name: str,
        source_resource_id: str,
        target_resource_id: str,
        steps: list[dict[str, Any]],
        risk_level: str = "low",
        rollback_enabled: bool = True,
    ) -> MigrationPlan:
        """Create a new migration plan"""

        plan = MigrationPlan(
            plan_id=plan_id,
            name=name,
            source_resource_id=source_resource_id,
            target_resource_id=target_resource_id,
            steps=steps,
            created_at=datetime.utcnow(),
            status="draft",
            risk_level=risk_level,
            rollback_enabled=rollback_enabled,
        )

        self._plans[plan_id] = plan
        return plan

    def get_plan(self, plan_id: str) -> MigrationPlan:
        """Retrieve a migration plan by ID"""
        if plan_id not in self._plans:
            raise ValueError(f"Migration plan '{plan_id}' not found")
        return self._plans[plan_id]

    def list_plans(self, status: str | None = None) -> list[MigrationPlan]:
        """List all migration plans, optionally filtered by status"""
        plans = list(self._plans.values())
        if status:
            plans = [p for p in plans if p.status == status]
        return plans

    def update_plan_status(self, plan_id: str, status: str) -> MigrationPlan:
        """Update the status of a migration plan"""
        plan = self.get_plan(plan_id)
        plan.status = status
        return plan

    def delete_plan(self, plan_id: str) -> bool:
        """Delete a migration plan"""
        if plan_id in self._plans:
            del self._plans[plan_id]
            return True
        return False
