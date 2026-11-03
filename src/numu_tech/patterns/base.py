"""Base migration patterns for common cloud migration scenarios"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MigrationPattern:
    """Base class for migration patterns"""

    name: str
    description: str
    source_types: list[str] = field(default_factory=list)
    target_types: list[str] = field(default_factory=list)
    parameters_schema: dict[str, Any] = field(default_factory=dict)

    def validate_params(self, params: dict[str, Any]) -> bool:
        """Validate pattern parameters against schema"""
        for required in self.parameters_schema.get("required", []):
            if required not in params:
                return False
        return True


class LiftAndShiftPattern(MigrationPattern):
    """Lift and shift migration pattern - minimal changes, direct migration"""

    def __init__(self):
        super().__init__(
            name="lift_and_shift",
            description="Direct migration with minimal code changes",
            source_types=["compute", "storage", "database"],
            target_types=["compute", "storage", "database"],
            parameters_schema={
                "required": ["instance_size", "region"],
                "properties": {
                    "instance_size": {"type": "string"},
                    "region": {"type": "string"},
                    "network": {"type": "string"},
                    "security_groups": {"type": "array"},
                },
            },
        )


class ReplatformPattern(MigrationPattern):
    """Replatform migration pattern - cloud-optimized but minimal changes"""

    def __init__(self):
        super().__init__(
            name="replatform",
            description="Cloud-optimized migration with minimal code changes",
            source_types=["compute", "database"],
            target_types=["compute", "database"],
            parameters_schema={
                "required": ["optimization_level", "target_service"],
                "properties": {
                    "optimization_level": {"type": "string", "enum": ["low", "medium", "high"]},
                    "target_service": {"type": "string"},
                    "cost_target": {"type": "number"},
                    "performance_target": {"type": "number"},
                },
            },
        )


class RefactorPattern(MigrationPattern):
    """Refactor pattern - re-architect for cloud-native"""

    def __init__(self):
        super().__init__(
            name="refactor",
            description="Re-architect for cloud-native capabilities",
            source_types=["compute", "database", "storage"],
            target_types=["compute", "database", "storage"],
            parameters_schema={
                "required": ["architecture_type", "data_strategy"],
                "properties": {
                    "architecture_type": {
                        "type": "string",
                        "enum": ["microservices", "serverless", "hybrid"],
                    },
                    "data_strategy": {
                        "type": "string",
                        "enum": ["migrate", "replatform", "rewrite"],
                    },
                    "deployment_method": {
                        "type": "string",
                        "enum": ["container", "function", "vm"],
                    },
                    "automation_level": {"type": "string", "enum": ["manual", "semi", "full"]},
                },
            },
        )


class RetirePattern(MigrationPattern):
    """Retire pattern - decommission unused resources"""

    def __init__(self):
        super().__init__(
            name="retire",
            description="Decommission unused or redundant resources",
            source_types=["compute", "storage", "database", "network"],
            target_types=[],
            parameters_schema={
                "required": ["confirmation", "backup_required"],
                "properties": {
                    "confirmation": {"type": "boolean"},
                    "backup_required": {"type": "boolean"},
                    "retention_days": {"type": "integer", "minimum": 0},
                },
            },
        )


class PatternLibrary:
    """Library of migration patterns"""

    def __init__(self):
        self._patterns: dict[str, MigrationPattern] = {}
        self._register_default_patterns()

    def _register_default_patterns(self) -> None:
        """Register default migration patterns"""
        patterns = [LiftAndShiftPattern(), ReplatformPattern(), RefactorPattern(), RetirePattern()]

        for pattern in patterns:
            self.register(pattern)

    def register(self, pattern: MigrationPattern) -> None:
        """Register a migration pattern"""
        self._patterns[pattern.name] = pattern

    def get_pattern(self, name: str) -> MigrationPattern | None:
        """Get a pattern by name"""
        return self._patterns.get(name)

    def list_patterns(self) -> list[str]:
        """List all available patterns"""
        return list(self._patterns.keys())

    def get_patterns_for_types(self, source_type: str, target_type: str) -> list[MigrationPattern]:
        """Get patterns suitable for source/target types"""
        matching = []
        for pattern in self._patterns.values():
            if source_type in pattern.source_types and target_type in pattern.target_types:
                matching.append(pattern)
        return matching
