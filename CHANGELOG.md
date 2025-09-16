# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-09-16

### Fixed
- Adjusted documentation link in `README` file
- Added `docs` in sdist to display logo on PyPI

## [0.1.4] - 2025-09-12

### Added
- Support for **multiple OS** and **Python version** in `CI`
- CHANGELOG and `toml` version check in `CI`
- `MKdocs` documentation with `CD` job to push on `GitHub Pages`
- Add automatic `git tag` and `GitHub release` based on CHANGELOG content in CD

### Changed
- Improved flexibility for `pytest` commands group by **overwriting** config at runtime
- Improved flexibility for `pytest` commands group by adding support for **any extra options** and testing specific classes or functions
- Improved flexibility for `lint` commands group by **overwriting** config at runtime

## [0.1.3] - 2025-08-29

### Added
- Continuous Integration Workflow
- Continuous Delivery Workflow

### Changed
- Improved console logs style

### Fixed
- Failing tests

## [0.1.0] - 2025-08-27

### Added
- Initial release of tidy-cli
- Code linting with ruff, mypy, and pydoclint
- Testing with pytest and coverage
- Rich CLI interface with progress indicators
- Configuration management for all tools
- Interactive and batch modes for linting