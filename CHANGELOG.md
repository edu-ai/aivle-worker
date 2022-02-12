# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.1.1] - 2021-10-15

### Added

- Easily test run aiVLE task bundle along with sample agent using `start_sandbox` function

## [0.1.2] - 2021-12-18

### Added

- `CELERY_CONCURRENCY` option in `.env` for configurable concurrency
- Upgrade pip before `pip install` to avoid Git parsing error
- Print stderr for `create_venv` subroutine

### Fixed

- Changed `create-venv.sh` to avoid Anaconda Python (which has an incompatible impl of virtualenv)

## [0.1.3] - 2022-02-01

### Added

- Resource monitoring: CPU/GPU utlization, RAM/VRAM usage
- Resource-sensitive load balance: pause consuming tasks whenever resource constraint is violated, automatically resume
  when appropriate

## [0.1.4] - 2022-02-12

### Added

- Runtime error report
- RAM limit for individual tasks