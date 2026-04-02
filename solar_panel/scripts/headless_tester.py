#!/usr/bin/env python3
"""
Headless serial tester for the solar panel app.

This script opens a serial device (from --port or SERIAL_PORT env var), reads
lines like `BATT:45` and `SOLAR:5.2`, and prints the parsed state. It does not
import or require any GUI libraries, so it can be used on systems without Qt.

Usage:
  python3 scripts/headless_tester.py --port /dev/pts/3
  # or
  SERIAL_PORT=/dev/pts/3 python3 scripts/headless_tester.py
"""
import os
import time
import argparse
import sys

BAUD_RATE = 9600


def parse_line(line, state):
    try:
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "BATT":
            state["battery"] = int(float(value))
        elif key == "SOLAR":
            state["solar"] = float(value)
        else:
            print("Unknown key:", key)
    except Exception:
        print("Bad data:", line)


def main():
    parser = argparse.ArgumentParser(description="Headless serial tester (no GUI required)")
    parser.add_argument("--port", help="serial device to open (overrides SERIAL_PORT env var)")
    parser.add_argument("--baud", type=int, default=BAUD_RATE, help="baud rate (default 9600)")
    args = parser.parse_args()

    port = args.port or os.environ.get("SERIAL_PORT")
    if not port:
        # try to auto-detect first available serial port if pyserial is present
        try:
            from serial.tools import list_ports

            ports = list_ports.comports()
            if ports:
                port = ports[0].device
                print("Auto-detected serial port:", port)
        except Exception:
            pass

    if not port:
        print("No serial port specified. Set SERIAL_PORT or pass --port.")
        return

    try:
        import serial
    except Exception as e:
        print("pyserial is required to run this tester. ImportError:", e)
        return

    try:
        ser = serial.Serial(port, args.baud, timeout=1)
    except Exception as e:
        print("Failed to open serial port:", e)
        return

    state = {"battery": None, "solar": None}

    print("Listening on", port)
    try:
        while True:
            try:
                line = ser.readline().decode(errors="ignore").strip()
            except Exception:
                print("Error reading from serial")
                break

            if line:
                parse_line(line, state)
                print("STATE:", state)
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        try:
            ser.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
