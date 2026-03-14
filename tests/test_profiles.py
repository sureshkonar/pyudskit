import json

from pyudskit import UDS
from pyudskit.profiles.schema import validate_profile


def test_profile_validation_dtc_format():
    data = {"dtcs": {"X1234": {"name": "Bad"}}}
    result = validate_profile(data)
    assert not result.ok


def test_profile_override_lookup(tmp_path):
    profile = {
        "name": "demo",
        "dids": {"0xF190": {"name": "VIN-OVERRIDE", "length_bytes": 17}},
        "dtcs": {"P0301": {"name": "Cylinder 1 Misfire"}},
    }
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile))
    uds = UDS(profile=str(path))
    assert "VIN-OVERRIDE" in uds.lookup_did(0xF190)
    assert "Cylinder 1 Misfire" in uds.explain_dtc("P0301")
