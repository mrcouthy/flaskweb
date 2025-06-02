# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - YYYY-MM-DD

### Added

-   Initial application structure with Flask.
-   User authentication (registration, login, logout, profile management).
-   Role-based authorization (admin and user roles) with `@admin_required` decorator.
-   Application organization using Blueprints (`auth` and `main`).
-   Dynamic side navigation menu based on authentication status and user role.
-   Basic styling with custom CSS (`static/css/style.css`) and Bootstrap integration (CDN).
-   Unit and integration tests for models, authentication, and authorization using `pytest`.
-   Database setup with Flask-SQLAlchemy, including initial admin user creation.
-   Configuration management (`config.py` and `tests/test_config.py`).
-   Requirements management (`requirements.txt`).
-   Basic `README.md` for setup and running the application.
