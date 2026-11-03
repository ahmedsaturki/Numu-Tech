# numu_tech.config.settings
"""Configuration module for Numu-Tech migration validation and rollback.

This module provides the MigrationConfig class used for demo initialization
and can be extended for production configuration needs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class MigrationConfig:
    """Configuration for migration operations.

    Attributes:
        dry_run: Whether to simulate rollback without actual changes
        rollback_timeout: Maximum time (seconds) for rollback operations
        validation_timeout: Maximum time (seconds) for validation checks
        retry_attempts: Number of retry attempts for failed operations
        enable_rollback: Whether rollback is enabled for this migration
        cloud_provider: Target cloud provider (azure, gcp, aws)
        region: Deployment region
        project_name: Name of the migration project
    """
    dry_run: bool = False
    rollback_timeout: int = 300
    validation_timeout: int = 120
    retry_attempts: int = 3
    enable_rollback: bool = True
    cloud_provider: str = "azure"
    region: str = "eastus"
    project_name: str = "phoenix-migration"
    additional_settings: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dict for serialization."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

# Default configuration for development
DEFAULT_CONFIG = MigrationConfig()
