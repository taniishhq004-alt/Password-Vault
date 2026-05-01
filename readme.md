# 🔐 Password Strength Analyser & Generator

**BCA 2nd Semester — Python Minor Project**

## 📌 About the Project

A personal **Password Vault** desktop application built with Python and Tkinter.
The app lets a single user store passwords for multiple apps (Instagram, Facebook, Snapchat, etc.) securely behind one master password.

### Key Features
- **Master Password Login** — SHA-256 hashed, never stored in plain text, with show/hide toggle
- **Password Strength Analyser** — visual strength bar, detailed feedback, NumPy-powered combination calculator
- **🌐 Live Breach Checker** — checks if your password was ever leaked in a real data breach using the HaveIBeenPwned API (k-anonymity — your password never leaves your PC)
- **Password Generator** — cryptographically secure passwords using Python's `secrets` module
- **Last 5 Password History Check** — rejects any generated password that matches a recent one
- **Fernet Encryption** — all saved passwords are AES-encrypted before writing to disk
- **Show / Hide Toggle** — reveal or hide passwords on screen
- **Delete Password** — remove any saved app password from the vault
- **📊 Analytics Dashboard** — pie chart of vault strength distribution, stat cards, oldest password tracker
- **Maroon & Black GUI** — built entirely with Tkinter

---

## 🛠️ Tech Stack

| Feature | Tool / Module |
|---|---|
| GUI | `tkinter`, `ttk` |
| Password Generation | `secrets`, `string` |
| Encryption / Decryption | `cryptography` (Fernet) |
| Hashing Master Password | `hashlib` (SHA-256) |
| Breach Checking | `requests` + HaveIBeenPwned API |
| Analytics & Charts | `matplotlib` |
| File Storage | `json` |
| Combinations Calculation | `numpy` |
| Date Handling | `datetime` |
| Background Threads | `threading` |

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
- `requests` library
- `matplotlib` library

---

## 🚀 How to Run

### Step 1 — Install required libraries

```bash
pip install cryptography numpy requests matplotlib
```

### Step 2 — Run the application

```bash
python password_vault.py
```

---

## 🖥️ App Screens

| Screen | Description |
|---|---|
| Login / Setup | First run: set master password. Later runs: enter to unlock. Show/hide toggle included. |
| Dashboard | Main menu with 4 options + Lock Vault |
| Analyse Password | Type any password → strength bar, feedback, NumPy combinations, live breach check |
| Generate & Save | Choose app name + length → generate strong password → save encrypted |
| View Saved | See all saved apps, reveal/hide passwords, delete entries |
| Analytics Dashboard | Pie chart of strength distribution, stat cards, oldest password warning |

---

## 🌐 How Breach Checker Works

The breach checker uses the **HaveIBeenPwned API** with a technique called **k-anonymity**:

1. Your password is hashed using SHA-1
2. Only the **first 5 characters** of the hash are sent to the API
3. The API returns all hashes starting with those 5 characters
4. The app checks locally if your full hash is in the list

**Your actual password never leaves your computer.** This is the same method used by professional password managers like 1Password and LastPass.

---

## 🔒 Security Details

- Master password is hashed with **SHA-256** and never stored as plain text
- All saved passwords are encrypted using **Fernet (AES-128-CBC)** from the `cryptography` library
- The Fernet encryption key is derived from your master password — no key file is stored separately
- `vault.json` is unreadable without the master password
- Password generation uses Python's `secrets` module (cryptographically secure random)
- Breach checking uses **k-anonymity** — real password never sent over internet

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
- **Networking** (`requests` — API calls)
- **Data Visualisation** (`matplotlib` — pie charts)
- **Multithreading** (`threading` — background API calls)

---

## 📝 Notes

- The app is single-user — one master password protects the entire vault
- If you forget your master password, the vault cannot be decrypted
- Deleting `vault.json` resets the app completely (all passwords lost)
- Breach checker requires an active internet connection
