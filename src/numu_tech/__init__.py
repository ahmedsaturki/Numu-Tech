"""Numu Tech - Zero-Pain Cloud Migration Automation Engine"""

__version__ = "0.2.0"
__author__ = "Ahmed Turki"
__email__ = "ahmed@numu.tech"

from .adapters.base import CloudAdapter
from .config.settings import MigrationConfig
from .core import MigrationEngine, MigrationPlan, MigrationResult, MigrationStatus, MigrationTarget
from .mappers.dependency import DependencyMapper
from .patterns.base import MigrationPattern
from .planning.engine import MigrationPlanner
from .risk.assessment import RiskAssessor
from .validation import MigrationValidator, RollbackLog, ValidationResult, ValidationStatus

__all__ = [
    "CloudAdapter",
    "DependencyMapper",
    "MigrationConfig",
    "MigrationEngine",
    "MigrationPattern",
    "MigrationPlan",
    "MigrationPlanner",
    "MigrationResult",
    "MigrationStatus",
    "MigrationTarget",
    "MigrationValidator",
    "RiskAssessor",
    "RollbackLog",
    "ValidationResult",
    "ValidationStatus",
]
