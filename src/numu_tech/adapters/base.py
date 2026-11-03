"""Base class for cloud provider adapters"""

from abc import ABC, abstractmethod
from typing import Any


class CloudAdapter(ABC):
    """Abstract base class for cloud provider adapters"""

    @abstractmethod
    async def migrate_compute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate compute resources"""

    @abstractmethod
    async def migrate_storage(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate storage resources"""

    @abstractmethod
    async def migrate_database(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate database resources"""

    @abstractmethod
    async def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate cloud configuration"""

    @abstractmethod
    async def create_rollback_plan(self, source_config: dict[str, Any]) -> dict[str, Any]:
        """Create a rollback plan for migration"""


class AzureAdapter(CloudAdapter):
    """Azure cloud provider adapter"""

    def __init__(self, credentials: dict[str, Any]):
        self.credentials = credentials

    async def migrate_compute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate Azure VMs to target"""
        # Implementation would use Azure SDK
        return {"migrated": [], "failed": []}

    async def migrate_storage(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate Azure Storage accounts"""
        return {"migrated": [], "failed": []}

    async def migrate_database(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate Azure SQL/PostgreSQL"""
        return {"migrated": [], "failed": []}

    async def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate Azure configuration"""
        required = ["subscription_id", "tenant_id", "client_id", "client_secret"]
        return all(k in config for k in required)

    async def create_rollback_plan(self, source_config: dict[str, Any]) -> dict[str, Any]:
        """Create Azure rollback plan"""
        return {"steps": [], "description": "Azure rollback plan"}


class AWSAdapter(CloudAdapter):
    """AWS cloud provider adapter"""

    def __init__(self, credentials: dict[str, Any]):
        self.credentials = credentials

    async def migrate_compute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate AWS EC2 instances"""
        return {"migrated": [], "failed": []}

    async def migrate_storage(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate AWS S3 buckets"""
        return {"migrated": [], "failed": []}

    async def migrate_database(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate AWS RDS/Aurora"""
        return {"migrated": [], "failed": []}

    async def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate AWS configuration"""
        required = ["access_key_id", "secret_access_key", "region"]
        return all(k in config for k in required)

    async def create_rollback_plan(self, source_config: dict[str, Any]) -> dict[str, Any]:
        """Create AWS rollback plan"""
        return {"steps": [], "description": "AWS rollback plan"}


class GCPAdapter(CloudAdapter):
    """Google Cloud Platform adapter"""

    def __init__(self, credentials: dict[str, Any]):
        self.credentials = credentials

    async def migrate_compute(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate GCP Compute Engine"""
        return {"migrated": [], "failed": []}

    async def migrate_storage(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate GCP Cloud Storage"""
        return {"migrated": [], "failed": []}

    async def migrate_database(self, params: dict[str, Any]) -> dict[str, Any]:
        """Migrate GCP Cloud SQL"""
        return {"migrated": [], "failed": []}

    async def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate GCP configuration"""
        required = ["project_id", "private_key", "client_email"]
        return all(k in config for k in required)

    async def create_rollback_plan(self, source_config: dict[str, Any]) -> dict[str, Any]:
        """Create GCP rollback plan"""
        return {"steps": [], "description": "GCP rollback plan"}
