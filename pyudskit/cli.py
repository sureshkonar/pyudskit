from __future__ import annotations

import argparse
import sys

from pyudskit import UDS
from pyudskit.ai import AIClient
from pyudskit.profiles import load_profile


def main() -> None:
    parser = argparse.ArgumentParser(prog="pyudskit")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_encode = sub.add_parser("encode", help="Encode a plain-English request")
    p_encode.add_argument("text", help="Description to encode")

    p_decode = sub.add_parser("decode", help="Decode UDS bytes")
    p_decode.add_argument("hex", help="Hex bytes")

    p_service = sub.add_parser("service", help="Explain a service")
    p_service.add_argument("service", help="Service name or SID")

    p_dtc = sub.add_parser("dtc", help="Explain a DTC")
    p_dtc.add_argument("code", help="DTC code, e.g. P0301")

    p_ai = sub.add_parser("ai", help="AI encode/decode")
    p_ai.add_argument("mode", choices=["encode", "decode"])
    p_ai.add_argument("value")

    p_profile = sub.add_parser("profile", help="OEM profile utilities")
    p_profile_sub = p_profile.add_subparsers(dest="profile_cmd", required=True)
    p_profile_validate = p_profile_sub.add_parser("validate", help="Validate OEM profile JSON")
    p_profile_validate.add_argument("path", help="Path to profile JSON")
    p_profile_show = p_profile_sub.add_parser("show", help="Show profile summary")
    p_profile_show.add_argument("path", help="Path to profile JSON")

    args = parser.parse_args()

    if args.cmd == "encode":
        uds = UDS()
        print(uds.encode(args.text))
    elif args.cmd == "decode":
        uds = UDS()
        print(uds.decode(args.hex))
    elif args.cmd == "service":
        uds = UDS()
        print(uds.explain_service(args.service))
    elif args.cmd == "dtc":
        uds = UDS()
        print(uds.explain_dtc(args.code))
    elif args.cmd == "ai":
        ai = AIClient()
        if args.mode == "encode":
            print(ai.encode(args.value))
        else:
            print(ai.decode(args.value))
    elif args.cmd == "profile":
        if args.profile_cmd == "validate":
            data = load_profile(args.path)
            # load_profile already validates; if it didn't raise, it's ok
            print(f"OK: {data.name}")
        elif args.profile_cmd == "show":
            data = load_profile(args.path)
            print(f"name: {data.name}")
            print(f"dids: {len(data.dids)}")
            print(f"routines: {len(data.routines)}")
            print(f"services: {len(data.services)}")
            print(f"dtcs: {len(data.dtcs)}")
        else:
            print("Unknown profile command")
            sys.exit(2)


if __name__ == "__main__":
    main()
