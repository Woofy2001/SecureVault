import win32com.client
import pythoncom  # Required for COM initialization in threads
import time
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb  # Modern theming for Tkinter
import threading

# Store detected USB devices (VID, PID)
seen_devices = set()

# Function to extract VID & PID
def extract_vid_pid(device_id):
    match = re.search(r"VID_([0-9A-F]+)&PID_([0-9A-F]+)", device_id, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)  # (VID, PID)
    return None, None

# Function to fetch more detailed device names
def get_usb_device_full_name(vid, pid):
    pythoncom.CoInitialize()  # Ensure COM is initialized
    wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\cimv2")
    devices = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity")

    for device in devices:
        device_id = getattr(device, "DeviceID", "")
        if f"VID_{vid}" in device_id and f"PID_{pid}" in device_id:
            return device.Name  # Return detailed device name
    return None  # If no better name is found, return None

# Function to update the GUI when a new USB is detected
def log_event(device, tree):
    global seen_devices
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_name = device.Name
    device_id = getattr(device, "DeviceID", "Unknown")
    manufacturer = getattr(device, "Manufacturer", "Unknown")

    vid, pid = extract_vid_pid(device_id)

    # Skip duplicates
    if vid and pid and (vid, pid) in seen_devices:
        return  

    # Get a more detailed name if available
    better_name = get_usb_device_full_name(vid, pid)
    if better_name:
        device_name = better_name  

    # Fix generic manufacturer names
    if manufacturer.lower() == "(standard keyboards)":
        manufacturer = "Generic Keyboard"
    elif manufacturer.lower() == "(standard system devices)":
        manufacturer = "Generic USB Device"
    elif manufacturer.lower() == "microsoft" and "razer" in device_name.lower():
        manufacturer = "Razer Inc."

    # Add to seen devices
    seen_devices.add((vid, pid))

    # Insert new row into the Treeview table
    tree.insert("", "end", values=(timestamp, device_name, manufacturer, vid, pid))

# Function to monitor USB insertions
def monitor_usb(tree):
    try:
        pythoncom.CoInitialize()  # ✅ Fix: Initialize COM in the thread
        wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator").ConnectServer(".", "root\cimv2")
        watcher = wmi.ExecNotificationQuery(
            "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_PnPEntity'"
        )

        while True:
            event = watcher.NextEvent()
            log_event(event.TargetInstance, tree)
            time.sleep(1)

    except Exception as e:
        print(f"❌ WMI Connection Failed: {str(e)}")

# GUI Setup
def create_gui():
    root = tb.Window(themename="superhero")  # Modern Tkinter theme
    root.title("USB Device Monitor")
    root.geometry("700x400")

    label = tb.Label(root, text="🔌 USB Monitoring Dashboard", font=("Arial", 16, "bold"))
    label.pack(pady=10)

    # Create table
    columns = ("Timestamp", "Device Name", "Manufacturer", "VID", "PID")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Define column headers
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    tree.pack(pady=20, padx=10, fill="both", expand=True)

    # Start monitoring USB devices in a separate thread
    monitor_thread = threading.Thread(target=monitor_usb, args=(tree,), daemon=True)
    monitor_thread.start()

    root.mainloop()

# Run GUI
if __name__ == "__main__":
    create_gui()
