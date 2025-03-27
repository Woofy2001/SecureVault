# 🔐 SecureVault – Personal File Encryption & Threat Detection Tool

SecureVault is a Python-based cybersecurity tool designed to protect sensitive files and detect suspicious system activity. It combines file encryption, USB monitoring, and file access logging into a single, modular application.

---

## 🚀 Features (Work in Progress)

- 🔒 **AES-256 File Encryption & Decryption**  
  Encrypt and decrypt files securely using symmetric encryption with Fernet.

- 🛡️ **USB Device Monitoring** *(coming soon)*  
  Detect and log unauthorized USB device connections.

- 🔍 **Suspicious File Access Logger** *(coming soon)*  
  Watch sensitive directories for unauthorized access or tampering.

- 📈 **Logs Viewer Dashboard** *(planned)*  
  View logs in a clean, user-friendly CLI or GUI interface.

---

## 🧠 Learning Objectives

- Cryptography: AES, RSA, hashing (SHA256)
- System monitoring and real-world logging
- Python scripting and modular code design
- Cybersecurity fundamentals

---

## 🛠️ Tech Stack

- Python
- `cryptography` – AES encryption via Fernet
- `watchdog` – file monitoring
- `pyudev` / `pywin32` – USB detection
- `rich`, `tkinter`, `flask` – for dashboards (planned)

---

## 📦 Project Structure

```
SecureVault/
│
├── encryption/          # File encryption module
│   └── encryptor.py     # Script for encrypting/decrypting files
│
├── usb_monitor/         # USB activity detection (WIP)
├── access_logger/       # File access logger (WIP)
├── dashboard/           # CLI/GUI dashboard (planned)
├── test_files/          # Sample files for testing
└── README.md            # You're here
```

---

## ✅ Setup & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Woofy2001/SecureVault.git
cd SecureVault
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate (Linux/macOS)
```

### 3. Install Dependencies
```bash
pip install cryptography
```

### 4. Test File Encryption
Create a test file:
```bash
echo "This is a top secret file!" > my_secret.txt
```

Then run:
```bash
python encryption/encryptor.py
```

### 5. Output
- `my_secret.txt.enc`: Encrypted version
- `my_secret.txt`: Recovered original after decryption

---

## 🧪 Progress Log

- [x] Basic AES encryption & decryption with Fernet
- [ ] Password-based key derivation (PBKDF2)
- [ ] USB monitoring module
- [ ] File access logger
- [ ] CLI/GUI dashboard for viewing logs

---

## 📸 Demo (Coming Soon)
Short screen recording of encryption + alert system in action.

---

## 👨‍💻 Author

**Induwara Jayakody** – [GitHub](https://github.com/Woofy2001)

---

## 📄 License

MIT License. Use freely and responsibly.
