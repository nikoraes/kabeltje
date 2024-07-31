import os
import subprocess
import sys
import threading
import webbrowser
from flask import Flask, render_template, jsonify, request
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.simulate_location import DtSimulateLocation

app = Flask(__name__)

connected_device = None
developer_mode_enabled = False


@app.route("/start_tunnel")
def start_tunnel():
    if sys.platform != "win32":
        return jsonify({"error": "Tunnel feature is only supported on Windows"})

    def run_tunnel():
        subprocess.run(
            [
                "powershell",
                "-NoExit",
                "Start-Process",
                "powershell",
                "-ArgumentList",
                "'-NoExit -Command \"python -m pymobiledevice3 remote tunneld\"'",
                "-Verb",
                "runAs",
            ],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

    threading.Thread(target=run_tunnel, daemon=True).start()
    return jsonify({"message": "Tunnel started successfully"})


@app.route("/")
def index():
    google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    return render_template("index.html", google_maps_api_key=google_maps_api_key)


@app.route("/device_info")
def get_device_info():
    global connected_device, developer_mode_enabled
    devices = list(usbmux.list_devices())

    if devices:
        connected_device = devices[0]
        lockdown = LockdownClient(connected_device.serial)
        developer_mode_enabled = (
            lockdown.get_value("com.apple.security.mac.amfi", "DeveloperModeStatus")
            == 1
        )
        return jsonify(
            {
                "connected": True,
                "name": lockdown.get_value(domain="", key="DeviceName"),
                "developer_mode": developer_mode_enabled,
            }
        )
    else:
        connected_device = None
        developer_mode_enabled = False
        return jsonify({"connected": False})


@app.route("/enable_developer_mode")
def enable_developer_mode():
    if not connected_device:
        return jsonify({"error": "No device connected"})

    lockdown = LockdownClient(connected_device.serial)
    # Note: This is a placeholder. The actual method to enable developer mode
    # may differ and might require user interaction on the device.
    lockdown.set_value(
        domain="com.apple.security.mac.amfi", key="DeveloperModeStatus", value=1
    )

    return jsonify({"message": "Developer mode enabled successfully"})


@app.route("/set_location", methods=["POST"])
def set_location():
    if not connected_device or not developer_mode_enabled:
        return jsonify({"error": "Device not ready or developer mode not enabled"})

    data = request.json
    latitude = data["latitude"]
    longitude = data["longitude"]

    lockdown = LockdownClient(connected_device.serial)
    simulate_location = DtSimulateLocation(lockdown=lockdown)

    try:
        simulate_location.set(latitude, longitude)
        return jsonify({"message": "Location set successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/get_current_location")
def get_current_location():
    if not connected_device or not developer_mode_enabled:
        return jsonify({"error": "Device not ready or developer mode not enabled"})

    lockdown = LockdownClient(connected_device.serial)
    simulate_location = DtSimulateLocation(lockdown=lockdown)

    try:
        location = simulate_location.get()
        return jsonify({"latitude": location.latitude, "longitude": location.longitude})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    webbrowser.open("http://localhost:5000")
    app.run(debug=True)
