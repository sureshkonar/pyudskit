from pyudskit import UDS

uds = UDS()

print(uds.ask("What is UDS?"))
print(uds.encode("Read the VIN"))
print(uds.decode("50 03 00 19 01 F4"))
print(uds.explain_dtc("P0301"))
