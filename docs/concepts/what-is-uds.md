# What is UDS?

If you are new to automotive diagnostics, start here.

## What is an ECU?

An ECU (Electronic Control Unit) is a specialized computer inside a vehicle. Modern cars have many ECUs: engine control, transmission, body control, infotainment, and more. Each ECU runs firmware and exposes diagnostic functions.

## What is OBD and how does UDS relate?

OBD-II is a standard interface for reading emissions-related diagnostics. UDS (Unified Diagnostic Services) is a more complete diagnostic protocol defined by ISO 14229. Many modern vehicles use UDS under the hood for far more than OBD-II: flashing firmware, configuration, security access, and deep diagnostics.

## What is ISO 14229?

ISO 14229 defines the UDS protocol: services (like "Read Data By Identifier"), response rules, error codes (NRCs), timing parameters, and session control.

## Client–Server Model

UDS is a client–server protocol:

- **Tester**: the diagnostic tool (your app).
- **ECU**: the server that answers requests.

## Physical Layers

UDS runs over multiple transports:

- **CAN (ISO 15765)**: most common in vehicles.
- **K-Line**: legacy vehicles.
- **DoIP (ISO 13400)**: UDS over Ethernet.

## Why engineers use UDS

- Flashing and programming ECUs
- Reading and clearing DTCs
- End-of-line configuration
- Actuator tests and calibration

## Analogy

Think of UDS as SSH into your car’s computers: structured commands with strict permissions and timing.

<!-- Diagram: Tester ↔ CAN Bus ↔ ECU -->
