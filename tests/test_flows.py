from pyudskit.client import UDS


def test_programming_flow_returns_string(mock_llm):
    mock_llm("flow")
    uds = UDS(api_key="test")
    out = uds.programming_flow()
    assert isinstance(out, str)
