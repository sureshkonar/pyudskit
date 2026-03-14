from __future__ import annotations

import argparse

from pyudskit import UDS
from pyudskit.ai import AIClient


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


if __name__ == "__main__":
    main()
