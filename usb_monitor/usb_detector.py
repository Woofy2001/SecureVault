import win32com.client
import time
from datetime import datetime
import win32gui
import win32con
import re

# Store seen Vendor ID (VID) + Product ID (PID) to avoid multiple logs
seen_devices = set()

def extract_vid_pid(device_id):
    """ Extract Vendor ID (VID) and Product ID (PID) from the Device ID string. """
    match = re.search(r"VID_([0-9A-F]+)&PID_([0-9A-F]+)", device_id, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)  # (VID, PID)
    return None, None

def get_usb_device_full_name(vid, pid):
    """ Fetch a more detailed USB device name using Win32_USBControllerDevice """
    wmi = win32com.client.GetObject("winmgmts:")
    devices = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity")

    for device in devices:
        device_id = getattr(device, "DeviceID", "")
        if f"VID_{vid}" in device_id and f"PID_{pid}" in device_id:
            return device.Name  # Return the detailed device name
    return None  # If no better name is found, return None

def show_popup(device_name, manufacturer):
    message = f"ALERT: New USB Detected!\nDevice: {device_name}\nManufacturer: {manufacturer}"
    win32gui.MessageBox(0, message, "USB Alert", win32con.MB_ICONWARNING | win32con.MB_OK)

def log_event(device):
    global seen_devices
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    device_name = device.Name
    device_id = getattr(device, "DeviceID", "Unknown")
    manufacturer = getattr(device, "Manufacturer", "Unknown")

    # Extract VID & PID
    vid, pid = extract_vid_pid(device_id)

    # Avoid duplicates
    if vid and pid and (vid, pid) in seen_devices:
        return  

    seen_devices.add((vid, pid))  # Mark this device as logged

    # Try fetching a more detailed device name
    better_name = get_usb_device_full_name(vid, pid)
    if better_name:
        device_name = better_name  # Use the more accurate name if available

    # Improve manufacturer name readability
    if manufacturer.lower() == "(standard keyboards)":
        manufacturer = "Generic Keyboard"
    elif manufacturer.lower() == "(standard system devices)":
        manufacturer = "Generic USB Device"
    elif manufacturer.lower() == "microsoft" and "razer" in device_name.lower():
        manufacturer = "Razer Inc."  # Fix Razer devices appearing as Microsoft

    # Clean log format
    log_entry = (
        f"🔌 [Detected USB Device]\n"
        f"📅 Timestamp: {timestamp}\n"
        f"💻 Device Name: {device_name}\n"
        f"🏭 Manufacturer: {manufacturer}\n"
        f"🆔 VID: {vid} | PID: {pid}\n"
        f"------------------------------\n"
    )

    print(log_entry)

    # Save to log file
    with open("usb_monitor/usb_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

    show_popup(device_name, manufacturer)

def monitor_usb():
    print("🛡️ USB Monitoring Started... Press Ctrl+C to stop.")
    wmi = win32com.client.GetObject("winmgmts:")
    watcher = wmi.ExecNotificationQuery(
        "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_PnPEntity'"
    )

    try:
        while True:
            event = watcher.NextEvent()
            log_event(event.TargetInstance)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")

if __name__ == "__main__":
    monitor_usb()
