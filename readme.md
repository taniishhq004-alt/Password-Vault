# 🔐 Password Strength Analyser & Generator
## 📌 About the Project

A personal **Password Vault** desktop application built with Python and Tkinter.  
The app lets a single user store passwords for multiple apps (Instagram, Facebook, Snapchat, etc.) securely behind one master password.

### Key Features
- **Master Password Login** — SHA-256 hashed, never stored in plain text
- **Password Strength Analyser** — visual strength bar, detailed feedback, NumPy-powered combination calculator
- **Password Generator** — cryptographically secure passwords using Python's `secrets` module
- **Last 5 Password History Check** — rejects any generated password that matches a recent one
- **Fernet Encryption** — all saved passwords are AES-encrypted before writing to disk
- **Show / Hide Toggle** — reveal or hide passwords on screen
- **Delete Password** — remove any saved app password from the vault
- **Maroon & Black GUI** — built entirely with Tkinter

---

## 🛠️ Tech Stack

| Feature | Tool / Module |
|---|---|
| GUI | `tkinter`, `ttk` |
| Password Generation | `secrets`, `string` |
| Encryption / Decryption | `cryptography` (Fernet) |
| Hashing Master Password | `hashlib` (SHA-256) |
| File Storage | `json` |
| Combinations Calculation | `numpy` |
| Date Handling | `datetime` |

---

## 📂 Project Files

```
PasswordAnalyser/
│
├── password_vault.py     ← Main application file (run this)
├── vault.json            ← Auto-created on first run (your encrypted vault)
└── README.md             ← This file
```

> `vault.json` is created automatically the first time you run the app. Do NOT share this file with anyone.

---

## ⚙️ Requirements

- Python 3.8 or above
- `cryptography` library
- `numpy` library

---

## 🚀 How to Run

### Step 1 — Install required libraries
Open your terminal / command prompt and run:

```bash
pip install cryptography numpy
```

### Step 2 — Run the application

```bash
python password_vault.py
```

---

## 🖥️ App Screens

| Screen | Description |
|---|---|
| Login / Setup | First run: set master password. Later runs: enter to unlock. |
| Dashboard | Main menu with 3 options + Lock Vault |
| Analyse Password | Type any password → see strength bar, feedback, and possible combinations |
| Generate & Save | Choose app name + length → generate strong password → save encrypted |
| View Saved | See all saved apps, reveal/hide passwords, delete entries |

---

## 🔒 Security Details

- Master password is hashed with **SHA-256** and never stored as plain text
- All saved passwords are encrypted using **Fernet (AES-128-CBC)** from the `cryptography` library
- The Fernet encryption key is derived from your master password — no key file is stored separately
- `vault.json` is unreadable without the master password
- Password generation uses Python's `secrets` module (cryptographically secure random)

---

## 📊 Python Topics Covered

- Variables and Data Types
- Conditional Statements (`if`, `elif`, `else`)
- Loops (`for`, `while`)
- Strings and String Operations
- Lists, Sets, Dictionaries
- Functions
- `random` / `secrets` Module
- `numpy` (password combination calculation)
- File Handling (`json.load`, `json.dump`)
- Basic Encryption and Decryption (`cryptography.fernet`)
- Exception Handling (`try`, `except`)
- Object-Oriented Programming (class-based Tkinter app)

---

## 📝 Notes

- The app is single-user — one master password protects the entire vault
- If you forget your master password, the vault cannot be decrypted
- Deleting `vault.json` resets the app completely (all passwords lost)

---

*Session: 2025-26 | Even Semester II*