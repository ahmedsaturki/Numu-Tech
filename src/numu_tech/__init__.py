"""Numu Tech - Zero-Pain Cloud Migration Automation Engine"""

__version__ = "0.2.0"
__author__ = "Ahmed Turki"
__email__ = "ahmed@numu.tech"

from .core import MigrationEngine, MigrationPlan, MigrationResult, MigrationTarget, MigrationStatus
from .adapters.base import CloudAdapter
from .mappers.dependency import DependencyMapper
from .patterns.base import MigrationPattern
from .planning.engine import MigrationPlanner
from .validation.rollback import MigrationValidator
from .risk.assessment import RiskAssessor

__all__ = [
    "MigrationEngine",
    "MigrationPlan", 
    "MigrationResult",
    "CloudAdapter",
    "DependencyMapper",
    "MigrationPattern",
    "MigrationTarget",
    "MigrationStatus",
    "MigrationPlanner",
    "MigrationValidator",
    "RiskAssessor"
]