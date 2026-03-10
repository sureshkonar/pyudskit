# Common Questions

**1. What is the difference between UDS and OBD-II?**
UDS is a full diagnostic protocol with many services; OBD-II is a subset focused on emissions.

**2. Why does my request return NRC 0x7F?**
`0x7F` is a negative response. Check the NRC byte for the specific reason.

**3. What is TesterPresent and do I need it?**
TesterPresent keeps sessions alive. Use it for long operations or extended sessions.

**4. How do I know which session a service requires?**
Consult the service table or switch to extended/programming if you receive `0x7E`/`0x7F`.

**5. What is a seed and a key in SecurityAccess?**
The ECU sends a seed, your tool computes a key using an OEM algorithm.

**6. What does RCRRP (0x78) mean and what should I do?**
It means the ECU accepted the request but needs more time. Wait and retry or listen for the final response.

**7. How do I read multiple DIDs in one request?**
Use `uds.read_dids([0xF190, 0xF186])`.

**8. Can pyuds connect to a real car?**
Yes, when paired with a transport (CAN or DoIP). pyuds focuses on encoding/decoding and workflows.

**9. What is the difference between pending and confirmed DTC?**
Pending is detected once; confirmed is verified across cycles.

**10. What are the P2 and P2* timers?**
P2 is normal response time; P2* is extended time after `0x78`.

**11. Why do I get `conditionsNotCorrect`?**
The ECU state is wrong (session, ignition, vehicle speed, etc.).

**12. What is a DID?**
A Data Identifier used to read or write ECU data.

**13. How do I clear DTCs?**
Use `uds.clear_dtcs()` which sends `14 FF FF FF`.

**14. Do I need security access to read data?**
Not always. Some DIDs require extended session or security access.

**15. What is a routine?**
A predefined ECU function executed via `RoutineControl (0x31)`.

**16. What does `serviceNotSupportedInActiveSession` mean?**
You are in the wrong session. Switch sessions and retry.
