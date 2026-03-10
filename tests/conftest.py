import pytest

from pyudskit.client import UDS


@pytest.fixture
def mock_llm(monkeypatch):
    def _mock(response_text: str):
        def _call(self, prompt: str) -> str:
            full_prompt = f"{self.session.context_header()}\n{prompt}"
            self.session.add("user", full_prompt)
            self.session.add("assistant", response_text)
            return response_text

        monkeypatch.setattr(UDS, "_call_llm", _call, raising=True)
        return response_text

    return _mock


@pytest.fixture
def uds_client(mock_llm):
    mock_llm('{"uds_bytes":"22 F1 90","service":"ReadDataByIdentifier","description":"Read VIN","plain_english":"VIN"}')
    return UDS(api_key="test")
