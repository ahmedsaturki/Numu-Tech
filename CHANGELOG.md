# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-11-04

### Added

- **Migration Validation & Rollback System** — `numu_tech.validation` module with `MigrationValidator`,
  async rollback orchestration, and full test coverage (44 tests passing).
- **Prospect Management CLI** — `numu prospects` command with `add`, `list`, `check`, `export`, `import` subcommands.
  Local-only JSON/CSV storage, zero external dependencies.
- **Core Architecture** — Modular design with adapters pattern, `CloudAdapter` ABC, `MigrationEngine` with
  explicit `STEP_METHODS` allowlist for security-hardened step dispatch.
- **GitHub Actions CI** — Automated pipeline running tests on Python 3.10, 3.11, and 3.12.

### Changed

- Replaced deprecated `datetime.utcnow()` with timezone-aware `datetime.now(timezone.utc)`.
- `register_adapter()` signature reverted to sync (was incorrectly made async during audit).
- Migration engine now uses `TYPE_CHECKING` guard to break `core` ↔ `adapters.base` import cycle.
- Narrowed migration `except` clause from bare `Exception` to `(ValueError, RuntimeError, KeyError)`.

### Removed

- `validate_config({})` check from `register_adapter()` (it always failed with empty config).
- `_utcnow_iso()` helper function (replaced by `datetime.now(timezone.utc).isoformat()`).
- `_dependency_mapper` instance (exports preserved in module).

### Fixed

- Step dispatch security: `getattr` replaced with explicit `STEP_METHODS` class variable allowlist.
- Type safety: `typing.cast` used where needed to satisfy `no-any-return` mypy strictness.