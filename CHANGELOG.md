# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub issue templates for bug reports and feature requests
- Pull request template for consistent PR submissions
- CI/CD workflow using GitHub Actions
- Automated testing on multiple Python versions (3.8-3.11)

## [1.0.0] - 2026-01-23

### Added
- Initial release of Cypher
- Dual scraping methods (Direct API + Selenium fallback)
- Advanced analytics engine with GPA calculation
- Input validation and security features
- CSV and Excel export functionality
- Comprehensive documentation (API.md, ARCHITECTURE.md, DEPLOYMENT.md)
- Complete test suite (unit, integration, benchmarks)
- Contribution guidelines and MIT license
- Production-ready deployment guides

### Security
- Environment-based configuration
- Input sanitization to prevent injection attacks
- No hardcoded credentials

### Performance
- API scraping method 63x faster than Selenium
- Optimized HTML/JSON parsing

## [0.9.0] - Pre-release

### Added
- Modular backend structure
- Flask REST API
- Selenium-based web scraping
- BeautifulSoup HTML parsing
- Basic analytics calculations

---

[Unreleased]: https://github.com/xorinf/cypher/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/xorinf/cypher/releases/tag/v1.0.0
