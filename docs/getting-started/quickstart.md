# Quick Start

A runnable five-step walkthrough.

## Step 1 — Import and initialize

```python
from pyuds import UDS
uds = UDS()
```

Expected output:

```python
(no output)
```

Explanation: this creates a `UDS` client instance with your API key pulled from `ANTHROPIC_API_KEY` and prepares an ECU context for future requests.

## Step 2 — Ask a plain English question

```python
uds.ask("What is UDS?")
```

Expected output:

```python
A plain-English explanation of UDS.
```

Explanation: pyuds sends the question to Claude with an ECU context header, and returns a concise explanation.

## Step 3 — Encode a request

```python
uds.encode("Read the VIN")  # → "22 F1 90"
```

Expected output:

```python
22 F1 90
```

Explanation: pyuds translates your intent into a UDS request PDU (service `0x22` and DID `0xF190`).

## Step 4 — Decode a response

```python
uds.decode("62 F1 90 57 30 4C 41 53 54 31 32 33 34 35 36 37 38")
```

Expected output:

```python
Positive response to ReadDataByIdentifier (VIN = W0LAST12345678)
```

Explanation: the response is parsed as a positive UDS response (`0x62`) and decoded into plain English.

## Step 5 — Explain a DTC

```python
uds.explain_dtc("P0301")
```

Expected output:

```python
P0301: Cylinder 1 misfire detected, with likely causes and steps to read/clear.
```

Explanation: pyuds uses DTC conventions (SAE J2012) and UDS service knowledge to explain the code and how to act on it.
