from pyudskit.registry.services import UDS_SERVICES
from pyudskit.registry.nrc import UDS_NRC
from pyudskit.registry.dids import COMMON_DIDS
from pyudskit.registry.dtc_status import DTC_STATUS_BITS, DTC_CATEGORIES


def test_all_services_have_required_keys():
    required = {"name", "group", "subfunctions", "description"}
    for service in UDS_SERVICES.values():
        assert required.issubset(service.keys())


def test_service_count_minimum_26():
    assert len(UDS_SERVICES) >= 26


def test_nrc_count_minimum_40():
    assert len(UDS_NRC) >= 40


def test_did_f190_is_vin():
    assert COMMON_DIDS[0xF190]["name"] == "VIN"


def test_did_range_f180_to_f19f_complete():
    for did in range(0xF180, 0xF1A0):
        assert did in COMMON_DIDS


def test_dtc_status_bits_are_powers_of_two():
    for bit in DTC_STATUS_BITS.keys():
        assert bit & (bit - 1) == 0


def test_dtc_categories_pnbu():
    for k in ["P", "N", "B", "U"]:
        if k == "N":
            assert k not in DTC_CATEGORIES
        else:
            assert k in DTC_CATEGORIES
