DTC_STATUS_BITS: dict[int, str] = {
    0x01: "testFailed",
    0x02: "testFailedThisMonitoringCycle",
    0x04: "pendingDTC",
    0x08: "confirmedDTC",
    0x10: "testNotCompletedSinceLastClear",
    0x20: "testFailedSinceLastClear",
    0x40: "testNotCompletedThisMonitoringCycle",
    0x80: "warningIndicatorRequested",
}

DTC_SEVERITY: dict[int, str] = {
    0x20: "maintenanceOnly",
    0x40: "checkAtNextHalt",
    0x60: "checkImmediately",
}

DTC_CATEGORIES: dict[str, str] = {
    "P": "Powertrain",
    "C": "Chassis",
    "B": "Body",
    "U": "Network / Communication",
}
