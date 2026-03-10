from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UDSSession:
    """
    Maintains multi-turn LLM conversation history AND tracks
    the ECU's current diagnostic state for contextual prompting.
    """

    history: list[dict] = field(default_factory=list)

    active_session: str = "defaultSession"
    security_level: int = 0
    communication_control: str = "enableRxAndTx"
    dtc_setting: str = "on"
    tester_present_active: bool = False

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})

    def reset(self) -> None:
        self.history.clear()
        self.active_session = "defaultSession"
        self.security_level = 0
        self.communication_control = "enableRxAndTx"
        self.dtc_setting = "on"
        self.tester_present_active = False

    def context_header(self) -> str:
        return (
            "[ECU Context] "
            f"session={self.active_session} "
            f"securityLevel={self.security_level} "
            f"dtcSetting={self.dtc_setting}"
        )

    def set_session(self, session_name: str) -> None:
        self.active_session = session_name

    def set_security_level(self, level: int) -> None:
        self.security_level = level

    def summary(self) -> dict:
        return {
            "active_session": self.active_session,
            "security_level": self.security_level,
            "communication_control": self.communication_control,
            "dtc_setting": self.dtc_setting,
            "tester_present_active": self.tester_present_active,
        }
