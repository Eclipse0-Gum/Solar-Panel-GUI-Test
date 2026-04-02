#!/usr/bin/env python3
"""
Small Arduino-like simulator that creates a pseudo-TTY (pty) pair
and writes example serial messages (BATT, SOLAR) to the master end.

Usage:
  python3 scripts/arduino_sim.py

It will print the device path you should point `SERIAL_PORT` at, for example:
  SIMULATOR_DEVICE=/dev/pts/3

Then run your app like:
  SERIAL_PORT=/dev/pts/3 python3 app.py

The script keeps running and emits periodic messages.
"""
import os
import pty
import time
import argparse
import random
import sys


def main():
    parser = argparse.ArgumentParser(description="Arduino serial simulator (BATT/SOLAR)")
    parser.add_argument("--interval", type=float, default=1.0, help="seconds between full updates")
    parser.add_argument("--start-batt", type=int, default=50, help="starting battery percent (0-100)")
    parser.add_argument("--noise", type=float, default=2.0, help="max random change per step for battery")
    args = parser.parse_args()

    master_fd, slave_fd = pty.openpty()
    slave_name = os.ttyname(slave_fd)

    # Inform the user which device to use for the app
    print(f"SIMULATOR_DEVICE={slave_name}")
    sys.stdout.flush()

    # Open master fd for writing raw bytes
    with os.fdopen(master_fd, "wb", buffering=0) as w:
        batt = args.start_batt
        try:
            while True:
                # random walk battery
                change = int(round(random.uniform(-args.noise, args.noise)))
                batt = max(0, min(100, batt + change))
                solar = round(max(0.0, random.uniform(0.0, 6.0)), 2)

                msg_batt = f"BATT:{batt}\n".encode()
                msg_solar = f"SOLAR:{solar}\n".encode()

                # send battery then solar
                w.write(msg_batt)
                time.sleep(args.interval / 2)
                w.write(msg_solar)
                time.sleep(args.interval / 2)
        except BrokenPipeError:
            # The reader likely closed the slave side
            print("Simulator: reader disconnected; exiting")


if __name__ == "__main__":
    main()
