# Changelog

All notable changes to pyudskit are documented here.
Format: [Keep a Changelog](https://keepachangelog.com)
Versioning: [Semantic Versioning](https://semver.org)

## [Unreleased]
### Planned
- Local DTC database (offline J2012 lookup)
- ECU simulator for integration testing
- Enhanced ISO-TP flow control handling
- DTC analytics dashboards

## [0.3.0] — 2026-03-14
### Added
- OEM profile overrides for services, DIDs, routines, and DTCs
- SecurityAccess key algorithm registry + seed→key helper
- DTC response parser for 0x59 frames
- Transport session client with 0x78 (RCRRP) handling
- Mock transport for tests and simulations
- JSON/YAML export helpers
- Docs coverage tests
- CLI profile tools (`profile validate`, `profile show`)
- Security API documentation

## [0.2.0] — 2026-03-14
### Added
- CAN transport layer via python-can
- DoIP transport layer
- Async client (AsyncUDS)
- CLI tool: `pyudskit encode "Read the VIN"`
- Services + AI layer modules

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
