import win32com.client
import pythoncom
import time
from datetime import datetime

def log_evenet(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] USB Inserted: {event.name}\n"
    print(log_entry)

    with open("usb_monitor/usb_log.txt","a") as f:
        f.write(log_entry)


class USBEventHandler:
    def OnDeviceArrived(self, device):
        log_event(device)

def monitor_usb():
    print("🛡️  USB Monitoring Started... Press Ctrl+C to stop.")

    wmi = win32com.client.GetObject("winmgmts:")
    watcher= wmi.ExecNotificationQuery(
        "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA 'Win32_USBHub'"
    )

    try:
        while True:
            event= watcher.NextEvent()
            log_evenet(event.TargetInstance)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")

if __name__ == "__main__":
    monitor_usb()