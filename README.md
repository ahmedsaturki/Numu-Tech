# Numu Tech - Zero-Pain Cloud Migration Automation Engine

A production-ready Python framework for automating cloud migrations with minimal disruption for Gulf contracting companies.

## Features

- **Multi-Cloud Support**: Azure, AWS, and GCP adapters with unified interface
- **Dependency Mapping**: Automatic dependency analysis and migration ordering
- **Migration Patterns**: Lift & Shift, Replatform, Refactor, Retire strategies
- **Risk Assessment**: Automated risk scoring and mitigation planning
- **Rollback Support**: Built-in rollback mechanisms for safe migrations
- **Planning Engine**: Intelligent migration planning with acceptance criteria

## Project Structure

```
Numu-Tech/
├── src/
│   └── numu_tech/
│       ├── __init__.py
│       ├── core.py              # Core engine, plans, and results
│       ├── adapters/
│       │   ├── __init__.py
│       │   └── base.py          # Cloud provider adapters
│       ├── mappers/
│       │   ├── __init__.py
│       │   └── dependency.py    # Dependency mapping engine
│       ├── patterns/
│       │   ├── __init__.py
│       │   └── base.py          # Migration pattern library
│       ├── risk/
│       │   ├── __init__.py
│       │   └── assessment.py    # Risk assessment module
│       ├── planning/
│       │   ├── __init__.py
│       │   └── engine.py        # Migration planning engine
│       └── validation/
│           ├── __init__.py
│           └── rollback.py      # Validation and rollback support
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_adapters.py
│   ├── test_mappers.py
│   ├── test_patterns.py
│   └── test_integration.py
├── examples/
│   └── azure_migration.py
├── scripts/
│   └── demo.py
├── pyproject.toml
└── README.md
```

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from numu_tech import MigrationEngine, MigrationTarget
from numu_tech.adapters import AzureAdapter, AWSAdapter
from numu_tech.mappers import DependencyMapper

# Initialize engine
engine = MigrationEngine()

# Register adapters
engine.register_adapter("azure", AzureAdapter(credentials={
    "subscription_id": "your-sub-id",
    "tenant_id": "your-tenant-id",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
}))

engine.register_adapter("aws", AWSAdapter(credentials={
    "access_key_id": "your-access-key",
    "secret_access_key": "your-secret-key",
    "region": "eastus"
}))

# Define source and target resources
source = MigrationTarget(
    id="prod-vm-001",
    name="Production VM",
    type="compute",
    provider="azure",
    region="eastus"
)

target = MigrationTarget(
    id="target-vm-001",
    name="Target VM",
    type="compute",
    provider="aws",
    region="us-east-1"
)

# Create migration plan
plan = engine.create_plan(
    plan_id="migration-001",
    name="Azure to AWS VM Migration",
    source=source,
    target=target,
    steps=[
        {
            "type": "migrate_compute",
            "provider": "azure",
            "params": {"instance_id": "prod-vm-001"}
        },
        {
            "type": "migrate_compute", 
            "provider": "aws",
            "params": {"target_instance": "target-vm-001"}
        }
    ]
)

# Execute migration
result = await engine.execute_plan("migration-001")
print(f"Success: {result.success}")
print(f"Migrated: {result.migrated_resources}")
print(f"Failed: {result.failed_resources}")
```

## Running Examples

```bash
# Run the demo script
python examples/validation_rollback_demo.py

# Run Azure migration example
python examples/azure_migration.py
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_core.py -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Ahmed Turki - Initial work - [GitHub](https://github.com/ahmedsaturki)
