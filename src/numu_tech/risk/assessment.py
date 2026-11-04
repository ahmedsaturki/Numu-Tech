"""Risk assessment module for cloud migrations"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from numu_tech.core import MigrationTarget


class RiskLevel(Enum):
    """Risk level enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskFactor:
    """A single risk factor in a migration"""

    name: str
    description: str
    level: RiskLevel
    mitigation: str
    impact_score: int = 0  # 1-10 scale


@dataclass
class MigrationRisk:
    """Overall risk assessment for a migration"""

    plan_id: str
    risk_score: float  # 0.0 to 1.0
    risk_level: RiskLevel
    factors: list[RiskFactor] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


class RiskAssessor:
    """Assesses migration risks and provides mitigation recommendations"""

    def __init__(self) -> None:
        self._risk_patterns: dict[str, list[RiskFactor]] = {}
        self._register_default_patterns()

    def _register_default_patterns(self) -> None:
        """Register default risk assessment patterns"""
        self._risk_patterns = {
            "compute_migration": [
                RiskFactor(
                    name="downtime_window",
                    description="Service downtime during migration",
                    level=RiskLevel.MEDIUM,
                    mitigation="Plan migration during maintenance window",
                    impact_score=6,
                ),
                RiskFactor(
                    name="performance_regression",
                    description="Potential performance degradation post-migration",
                    level=RiskLevel.MEDIUM,
                    mitigation="Benchmark both environments before and after",
                    impact_score=5,
                ),
            ],
            "database_migration": [
                RiskFactor(
                    name="data_integrity",
                    description="Data integrity issues during transfer",
                    level=RiskLevel.HIGH,
                    mitigation="Implement checksum verification and rollback strategy",
                    impact_score=8,
                ),
                RiskFactor(
                    name="schema_compatibility",
                    description="Schema differences between source and target",
                    level=RiskLevel.MEDIUM,
                    mitigation="Run schema validation before full migration",
                    impact_score=6,
                ),
            ],
            "network_migration": [
                RiskFactor(
                    name="dns_propagation",
                    description="DNS changes may cause temporary outages",
                    level=RiskLevel.LOW,
                    mitigation="Set low TTL values before migration",
                    impact_score=3,
                ),
                RiskFactor(
                    name="security_group_mismatch",
                    description="Security group rules may not transfer correctly",
                    level=RiskLevel.HIGH,
                    mitigation="Audit and validate all security rules",
                    impact_score=7,
                ),
            ],
        }

    def assess_migration_risk(
        self,
        plan_id: str,
        source: MigrationTarget,
        target: MigrationTarget,
        steps: list[dict[str, Any]],
    ) -> MigrationRisk:
        """Assess overall migration risk based on plan details"""
        all_factors: list[RiskFactor] = []
        total_impact = 0
        recommendations: list[str] = []

        for step in steps:
            step_type = step.get("type", "generic")
            patterns = self._risk_patterns.get(step_type, [])
            all_factors.extend(patterns)
            total_impact += sum(f.impact_score for f in patterns)

            # Add specific recommendations based on step type
            recommendations.extend([f"Review {step_type} migration strategy" for _ in patterns])

        # Add provider-specific risks
        if source.provider != target.provider:
            all_factors.append(
                RiskFactor(
                    name="cross_provider_compatibility",
                    description="Cross-cloud compatibility issues",
                    level=RiskLevel.HIGH,
                    mitigation="Validate API compatibility between providers",
                    impact_score=8,
                )
            )
            recommendations.append("Test API compatibility in staging environment")

        # Calculate overall risk score
        max_possible_impact = len(all_factors) * 10
        risk_score = total_impact / max_possible_impact if max_possible_impact > 0 else 0.0

        # Determine risk level
        if risk_score < 0.3:
            risk_level = RiskLevel.LOW
        elif risk_score < 0.5:
            risk_level = RiskLevel.MEDIUM
        elif risk_score < 0.7:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL

        return MigrationRisk(
            plan_id=plan_id,
            risk_score=risk_score,
            risk_level=risk_level,
            factors=all_factors,
            recommendations=list(set(recommendations)),
        )
