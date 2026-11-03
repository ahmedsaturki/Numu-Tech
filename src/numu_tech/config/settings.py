from dataclasses import dataclass
from typing import Any


@dataclass
class MigrationConfig:
    dry_run: bool = False
    rollback_timeout: int = 300
    validation_timeout: int = 120
    retry_attempts: int = 3
    enable_rollback: bool = True
    cloud_provider: str = "azure"
    region: str = "eastus"
    project_name: str = "phoenix-migration"
    additional_settings: dict[str, Any] | None = None
