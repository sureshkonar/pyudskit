"""
pyudskit — Talk to your ECU in plain English.

LLM-powered ISO 14229 UDS assistant for automotive diagnostics.

    >>> from pyudskit import UDS
    >>> uds = UDS()
    >>> uds.encode("Read the VIN")
    '22 F1 90'
"""

from pyudskit.client import UDS
from pyudskit.message import UDSMessage
from pyudskit.session import UDSSession
from pyudskit.ai.client import AIClient
from pyudskit import services

__version__ = "0.2.0"
__all__ = ["UDS", "UDSMessage", "UDSSession", "AIClient", "services"]
