# Changelog

All notable changes to pyuds are documented here.
Format: [Keep a Changelog](https://keepachangelog.com)
Versioning: [Semantic Versioning](https://semver.org)

## [Unreleased]
### Planned
- CAN transport layer via python-can
- DoIP transport layer
- Local DTC database (offline J2012 lookup)
- Async client (AsyncUDS)
- CLI tool: `pyuds encode "Read the VIN"`

## [0.1.0] — 2025-01-01
### Added
- Initial release
- Full ISO 14229-1 service registry (26 services)
- All 40+ Negative Response Codes
- Standard DID registry (0xF180–0xF19F)
- DTC status bit decoder
- UDSMessage PDU parser
- UDSSession conversation + ECU state tracking
- UDSLLM class with beginner and advanced methods
- 6 diagnostic flow walkthroughs
- 30+ pytest tests
