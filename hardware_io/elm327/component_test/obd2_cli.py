#!/usr/bin/env python3

from __future__ import annotations

import argparse

from hardware_io.automotive.obd2.elm327 import Elm327Adapter
from hardware_io.automotive.obd2.obd2_errors import (
    Obd2CommandError,
    Obd2ConnectionError,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OBD-II adapter component test"
    )

    parser.add_argument(
        "--port",
        default="/dev/rfcomm0",
        help="Serial device path, such as /dev/rfcomm0",
    )

    parser.add_argument(
        "--baud",
        type=int,
        default=38400,
        help="Serial baud rate",
    )

    parser.add_argument(
        "--command",
        help="Send one command and exit, such as ATI or 010C",
    )

    return parser.parse_args()


def print_response(command: str, raw: str, lines: tuple[str, ...]) -> None:
    print(f"\nCommand: {command}")
    print("Response:")

    if lines:
        for line in lines:
            print(f"  {line}")
    else:
        print("  <empty>")

    print("\nRaw response:")
    print(repr(raw))


def run_single_command(
    adapter: Elm327Adapter,
    command: str,
) -> None:
    response = adapter.send_command(command)

    print_response(
        command=response.command,
        raw=response.raw,
        lines=response.lines,
    )


def run_interactive(adapter: Elm327Adapter) -> None:
    print("Connected.")
    print("Enter an OBD-II or ELM327 command.")
    print("Examples: ATI, ATDP, 0100, 010C, 010D")
    print("Enter 'quit' or 'exit' to stop.\n")

    while True:
        try:
            command = input("obd2> ").strip()
        except EOFError:
            print()
            break

        if not command:
            continue

        if command.lower() in {"quit", "exit"}:
            break

        try:
            response = adapter.send_command(command)

            print_response(
                command=response.command,
                raw=response.raw,
                lines=response.lines,
            )

        except Obd2CommandError as exc:
            print(f"Command error: {exc}")


def main() -> None:
    args = parse_args()

    adapter = Elm327Adapter(
        port=args.port,
        baud=args.baud,
    )

    try:
        print(
            f"Connecting to ELM327 on "
            f"{args.port} at {args.baud} baud..."
        )

        adapter.connect()

        if args.command:
            run_single_command(adapter, args.command)
        else:
            run_interactive(adapter)

    except Obd2ConnectionError as exc:
        print(f"Connection error: {exc}")
        raise SystemExit(1) from exc

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        adapter.disconnect()


if __name__ == "__main__":
    main()
