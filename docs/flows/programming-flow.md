# Programming Flow

A full ECU flash programming walkthrough.

## Sequence Diagram

```python
Tester                              ECU
  │── 10 03 (ExtendedSession) ──────►│
  │◄── 50 03 00 19 01 F4 ────────────│
  │── 28 03 (DisableComms) ─────────►│
  │── 85 02 (DTCSetting OFF) ───────►│
  │── 27 01 (RequestSeed) ──────────►│
  │◄── 67 01 [seed bytes] ───────────│
  │── 27 02 [key bytes] ────────────►│
  │◄── 67 02 ────────────────────────│
  │── 10 02 (ProgrammingSession) ───►│
  │── 31 01 FF 00 (EraseFlash) ─────►│
  │◄── 71 01 FF 00 ──────────────────│
  │── 34 ... (RequestDownload) ─────►│
  │◄── 74 ... ───────────────────────│
  │── 36 01 [data] (TransferData) ──►│  ← repeat per block
  │◄── 76 01 ────────────────────────│
  │── 37 (RequestTransferExit) ─────►│
  │◄── 77 ───────────────────────────│
  │── 31 01 FF 02 (CheckDeps) ──────►│
  │── 11 01 (HardReset) ────────────►│
```

## Step-by-step

1. **Switch to extended session (0x10 03)**
   - Needed to access security and programming setup services.
   - If rejected: NRC `0x7E` or `0x7F`.

2. **Disable communications (0x28 03)**
   - Prevents network traffic during programming.
   - If rejected: NRC `0x31`.

3. **Disable DTC setting (0x85 02)**
   - Avoids DTCs during flashing.
   - If rejected: NRC `0x7E`.

4. **Security access (0x27)**
   - Request seed → compute key → send key.
   - If rejected: NRC `0x35`, `0x36`, `0x37`.

5. **Switch to programming session (0x10 02)**
   - Enables download services.

6. **Erase flash (0x31 01 FF00)**
   - RoutineControl start for erase routine.

7. **Request download (0x34)**
   - Provide address and length.
   - If rejected: NRC `0x70`.

8. **Transfer data (0x36)**
   - Send blocks in order.
   - If rejected: NRC `0x73`.

9. **Request transfer exit (0x37)**
   - Finalize data transfer.

10. **Check dependencies (0x31 01 FF02)**
    - Optional routine to verify programming dependencies.

11. **ECU reset (0x11 01)**
    - Reboot into new software.

## Timing Notes

- Respect `P2Server_max` and `P2*Server_max` when waiting for responses.
- Erase and transfer steps can trigger `0x78` pending responses.

## pyuds Code

```python
from pyuds import UDS

uds = UDS()

uds.switch_session("extended")
uds.communication_control("disable")
uds.control_dtc_setting("off")
uds.security_access_flow(level=1)
uds.switch_session("programming")
uds.routine_control(0xFF00, "start")
uds.request_download(0x08000000, 0x10000)
uds.transfer_data(0x01, "AA BB CC ...")
uds.request_transfer_exit()
uds.ecu_reset("hard")
```

!!! warning "Safety"
    Flashing ECUs can brick hardware if interrupted. Ensure stable power and correct files.
