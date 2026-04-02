import os
import time
import threading
import logging

import serial
from serial.tools import list_ports

import pyvisual as pv
from ui.ui import create_ui, set_arduino

# ================================
# CONFIG / LOGGING
# ================================
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

BAUD_RATE = 9600

# Try env var first, then auto-detect first available serial port
SERIAL_PORT = os.environ.get("SERIAL_PORT")
if not SERIAL_PORT:
    try:
        ports = list_ports.comports()
        if ports:
            SERIAL_PORT = ports[0].device
            logging.info(f"Auto-detected serial port: {SERIAL_PORT}")
        else:
            SERIAL_PORT = None
    except Exception:
        SERIAL_PORT = None

# ================================
# SERIAL SETUP
# ================================
arduino = None
if SERIAL_PORT:
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logging.info(f"Opened serial port {SERIAL_PORT} @ {BAUD_RATE} baud")
    except serial.SerialException as e:
        arduino = None
        logging.warning(f"Unable to open serial port {SERIAL_PORT}: {e}")
else:
    logging.warning("No serial port configured or detected; running without Arduino")

# ================================
# GLOBAL STATE
# ================================
system_data = {
    "battery": 0,
    "solar": 0,
}


def read_serial(ui):
    while True:
        if arduino and getattr(arduino, "in_waiting", 0):
            try:
                line = arduino.readline().decode(errors="ignore").strip()
                if line:
                    parse_data(line, ui)
            except Exception:
                logging.exception("Error reading serial data")
        else:
            # avoid busy-waiting
            time.sleep(0.1)


def parse_data(line, ui):
    """
    Example messages:
    BATT:45
    SOLAR:5.2
    """
    try:
        key, value = line.split(":", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "BATT":
            val = int(float(value))
            system_data["battery"] = val

            # Update progress bar if UI is available
            if ui and "page_0" in ui and "Progressbar_0" in ui["page_0"]:
                try:
                    ui["page_0"]["Progressbar_0"].value = val
                except Exception:
                    logging.exception("Failed updating Progressbar_0")

        elif key == "SOLAR":
            system_data["solar"] = float(value)

    except Exception:
        logging.warning("Bad data: %s", line)


def attach_events(ui):
    if not ui or "page_0" not in ui:
        return

    # NOTE: key in ui_page_0 is "Power_slider" (not "Slider_1")
    slider = ui["page_0"].get("Power_slider")
    if slider is None:
        logging.debug("Power_slider not present in UI; skipping event attach")
        return

    def on_slider_change(value):
        if arduino:
            try:
                cmd = f"POWER:{int(value)}\n"
                arduino.write(cmd.encode())
                logging.info("Sent: %s", cmd.strip())
            except Exception:
                logging.exception("Failed to send POWER command to Arduino")

    # attach callback (library uses .on_change in current codebase)
    slider.on_change = on_slider_change


def main():
    app = pv.PvApp()
    # pass arduino into UI so callbacks (button) are wired immediately
    ui = create_ui(arduino)

    # If you created UI before opening serial, you can also call:
    # set_arduino(ui, arduino)

    attach_events(ui)

    # Start serial listener thread
    threading.Thread(target=read_serial, args=(ui,), daemon=True).start()

    ui["window"].show()
    app.run()


if __name__ == "__main__":
    main()