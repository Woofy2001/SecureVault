import win32com.client
import time
import re
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live

# Initialize console for Rich CLI
console = Console()

# Store seen devices (VID, PID) to avoid duplicate logging
seen_devices = set()

# Function to extract Vendor ID (VID) & Product ID (PID)
def extract_vid_pid(device_id):
    match = re.search(r"VID_([0-9A-F]+)&PID_([0-9A-F]+)", device_id, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)  # (VID, PID)
    return None, None

# Function to fetch a more detailed device name
def get_usb_device_full_name(vid, pid):
    wmi = win32com.client.GetObject("winmgmts:")
    devices = wmi.ExecQuery("SELECT * FROM Win32_PnPEntity")

    for device in devices:
        device_id = getattr(device, "DeviceID", "")
        if f"VID_{vid}" in device_id and f"PID_{pid}" in device_id:
            return device.Name  # Return detailed device name
    return None  # If no better name is found, return None

# Function to generate a Rich table for real-time USB logs
def generate_usb_table():
    table = Table(title="🔌 USB Device Monitor", show_lines=True)
    table.add_column("Timestamp", style="cyan", justify="center")
    table.add_column("Device Name", style="magenta", justify="left")
    table.add_column("Manufacturer", style="green", justify="left")
    table.add_column("VID", style="yellow", justify="center")
    table.add_column("PID", style="yellow", justify="center")

    for device in seen_devices:
        table.add_row(*device)

    return table

# Function to log USB events in real-time
def log_event(device):
    global seen_devices
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_name = device.Name
    device_id = getattr(device, "DeviceID", "Unknown")
    manufacturer = getattr(device, "Manufacturer", "Unknown")

    vid, pid = extract_vid_pid(device_id)

    # Skip duplicates
    if vid and pid and (vid, pid) in [(d[3], d[4]) for d in seen_devices]:
        return  

    # Get better device name if available
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
    seen_devices.add((timestamp, device_name, manufacturer, vid, pid))

# Function to monitor USB insertions
def monitor_usb():
    console.print("[bold green]🛡️ USB Monitoring Started... Press Ctrl+C to stop.[/bold green]")
    wmi = win32com.client.GetObject("winmgmts:")
    watcher = wmi.ExecNotificationQuery(
        "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_PnPEntity'"
    )

    with Live(generate_usb_table(), refresh_per_second=1) as live:
        try:
            while True:
                event = watcher.NextEvent()
                log_event(event.TargetInstance)
                live.update(generate_usb_table())  # Refresh table on new USB insert
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[bold red]🛑 Monitoring stopped.[/bold red]")

# Run the script
if __name__ == "__main__":
    monitor_usb()
