COMMON_ROUTINES: dict[int, dict] = {
    0x0202: {
        "name": "CheckProgrammingPreConditions",
        "description": "Verify ECU is ready to enter programming session",
        "session_required": "extended",
    },
    0xFF00: {
        "name": "EraseFlashMemory",
        "description": "Erase the ECU flash memory region before download",
        "session_required": "programming",
    },
    0xFF01: {
        "name": "CheckFlashMemory",
        "description": "Verify CRC/checksum of downloaded flash data",
        "session_required": "programming",
    },
    0xFF02: {
        "name": "CheckProgrammingDependencies",
        "description": "Validate compatibility of newly programmed software",
        "session_required": "programming",
    },
    0x0203: {
        "name": "EraseMemory",
        "session_required": "programming",
        "description": "Erase memory region before programming",
    },
    0x0204: {
        "name": "ResetToDefaultSettings",
        "session_required": "extended",
        "description": "Reset ECU settings to defaults",
    },
    0xF000: {
        "name": "VariantCoding",
        "session_required": "extended",
        "description": "Write variant coding data",
    },
    0xF001: {
        "name": "ReadVariantCoding",
        "session_required": "extended",
        "description": "Read variant coding data",
    },
}
