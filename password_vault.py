import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
import secrets
import string
import numpy as np
from datetime import date
from cryptography.fernet import Fernet
import base64

# ─────────────────────────────────────────────
#  CONSTANTS & PATHS
# ─────────────────────────────────────────────
VAULT_FILE = "vault.json"
KEY_FILE   = "vault.key"

BG        = "#0a0a0a"
BG2       = "#1a1a1a"
MAROON    = "#800000"
MAROON_DK = "#5c0000"
WHITE     = "#ffffff"
GREY      = "#888888"
RED       = "#ff4444"
ORANGE    = "#ff8800"
GREEN     = "#00cc44"
BORDER    = "#2a2a2a"

FONT_TITLE  = ("Segoe UI", 15, "bold")
FONT_SUB    = ("Segoe UI", 9)
FONT_BODY   = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Courier New", 11)
FONT_SMALL  = ("Segoe UI", 8)

# ─────────────────────────────────────────────
#  ENCRYPTION HELPERS
# ─────────────────────────────────────────────
def derive_key(master_password: str) -> bytes:
    """Derive a Fernet key from master password using SHA-256."""
    digest = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_password(plain: str, master_password: str) -> str:
    key = derive_key(master_password)
    return Fernet(key).encrypt(plain.encode()).decode()

def decrypt_password(token: str, master_password: str) -> str:
    key = derive_key(master_password)
    return Fernet(key).decrypt(token.encode()).decode()

def hash_master(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────────
#  VAULT FILE HELPERS
# ─────────────────────────────────────────────
def load_vault() -> dict:
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "r") as f:
        return json.load(f)

def save_vault(data: dict):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────────
#  PASSWORD ANALYSIS
# ─────────────────────────────────────────────
def analyse_password(pwd: str) -> dict:
    length      = len(pwd)
    has_upper   = any(c.isupper() for c in pwd)
    has_lower   = any(c.islower() for c in pwd)
    has_digit   = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)

    score = 0
    feedback = []

    # Length scoring
    if length >= 16:
        score += 30
    elif length >= 12:
        score += 20
    elif length >= 8:
        score += 10
        feedback.append(("warn", "Use 12+ characters for better security"))
    else:
        score += 0
        feedback.append(("warn", "Too short — use at least 8 characters"))

    if has_upper:
        score += 15
        feedback.append(("ok", "Has uppercase letters"))
    else:
        feedback.append(("warn", "Add uppercase letters (A-Z)"))

    if has_lower:
        score += 15
        feedback.append(("ok", "Has lowercase letters"))
    else:
        feedback.append(("warn", "Add lowercase letters (a-z)"))

    if has_digit:
        score += 20
        feedback.append(("ok", "Contains numbers"))
    else:
        feedback.append(("warn", "Add numbers (0-9)"))

    if has_special:
        score += 20
        feedback.append(("ok", "Contains special characters"))
    else:
        feedback.append(("warn", "Add special characters (!@#$...)"))

    # Bonus for length
    if length >= 20:
        score = min(score + 10, 100)
        feedback.append(("ok", "Excellent length (20+ characters)"))

    score = min(score, 100)

    if score >= 80:
        label = "Very Strong"
        color = GREEN
    elif score >= 60:
        label = "Strong"
        color = "#88dd00"
    elif score >= 40:
        label = "Medium"
        color = ORANGE
    else:
        label = "Weak"
        color = RED

    # NumPy: calculate possible combinations
    charset_size = 0
    if has_lower:   charset_size += 26
    if has_upper:   charset_size += 26
    if has_digit:   charset_size += 10
    if has_special: charset_size += 32
    if charset_size == 0: charset_size = 26

    combinations = np.power(float(charset_size), float(length))

    return {
        "score": score,
        "label": label,
        "color": color,
        "feedback": feedback,
        "combinations": combinations,
        "charset_size": charset_size,
        "length": length
    }

# ─────────────────────────────────────────────
#  PASSWORD GENERATOR
# ─────────────────────────────────────────────
def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Ensure all character types are present
        if (any(c.isupper() for c in pwd) and
            any(c.islower() for c in pwd) and
            any(c.isdigit() for c in pwd) and
            any(c in string.punctuation for c in pwd)):
            return pwd

# ─────────────────────────────────────────────
#  REUSABLE UI HELPERS
# ─────────────────────────────────────────────
def styled_frame(parent, bg=BG, **kw):
    return tk.Frame(parent, bg=bg, **kw)

def label(parent, text, font=FONT_BODY, fg=WHITE, bg=BG, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def entry(parent, show=None, font=FONT_BODY, width=28):
    e = tk.Entry(parent, show=show, font=font, width=width,
                 bg=BG2, fg=WHITE, insertbackground=WHITE,
                 relief="flat", bd=0,
                 highlightthickness=1, highlightbackground=MAROON,
                 highlightcolor=MAROON)
    return e

def btn(parent, text, command, bg=MAROON, fg=WHITE, font=FONT_BOLD, width=20, pady=7):
    b = tk.Button(parent, text=text, command=command,
                  bg=bg, fg=fg, font=font, width=width,
                  relief="flat", bd=0, cursor="hand2",
                  activebackground=MAROON_DK, activeforeground=WHITE,
                  pady=pady)
    b.bind("<Enter>", lambda e: b.config(bg=MAROON_DK))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b

def outline_btn(parent, text, command, width=20):
    b = tk.Button(parent, text=text, command=command,
                  bg=BG, fg=MAROON, font=FONT_BOLD, width=width,
                  relief="flat", bd=0, cursor="hand2",
                  highlightthickness=1, highlightbackground=MAROON,
                  highlightcolor=MAROON,
                  activebackground=BG2, activeforeground=MAROON,
                  pady=6)
    return b

def separator(parent, bg=BORDER):
    return tk.Frame(parent, bg=bg, height=1)

def section_title(parent, text):
    f = styled_frame(parent)
    tk.Frame(f, bg=MAROON, width=4, height=20).pack(side="left", padx=(0, 8))
    label(f, text, font=FONT_BOLD, fg=WHITE).pack(side="left")
    return f

# ─────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────
class PasswordVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Vault")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.master_password = None
        self._center(420, 520)
        self.show_login()

    def _center(self, w, h):
        self.root.geometry(f"{w}x{h}")
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ── Header bar ───────────────────────────
    def _header(self, title, show_back=False, back_cmd=None):
        bar = tk.Frame(self.root, bg=MAROON, height=48)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        if show_back and back_cmd:
            tk.Button(bar, text="← Back", bg=MAROON, fg="#ffcccc",
                      font=FONT_SMALL, relief="flat", bd=0,
                      activebackground=MAROON_DK, activeforeground=WHITE,
                      cursor="hand2", command=back_cmd).pack(side="left", padx=10)

        tk.Label(bar, text=title, bg=MAROON, fg=WHITE,
                 font=("Segoe UI", 12, "bold")).pack(side="left", padx=(10 if not show_back else 0, 0), pady=12)

    # ══════════════════════════════════════════
    #  SCREEN 1 — LOGIN / SETUP
    # ══════════════════════════════════════════
    def show_login(self):
        self.clear()
        self._center(400, 460)

        vault = load_vault()
        is_new = "master_hash" not in vault

        self._header("🔐  Password Vault")

        body = styled_frame(self.root, padx=40, pady=30)
        body.pack(fill="both", expand=True)

        # Lock icon area
        icon_frame = styled_frame(body)
        icon_frame.pack(pady=(10, 20))
        tk.Frame(icon_frame, bg=MAROON, width=56, height=56,
                 relief="flat").pack()
        canvas = tk.Canvas(icon_frame, width=56, height=56, bg=MAROON,
                           highlightthickness=0)
        canvas.place(x=0, y=0)
        canvas.create_rectangle(14, 26, 42, 46, fill=WHITE, outline="")
        canvas.create_arc(18, 12, 38, 34, start=0, extent=180,
                          outline=WHITE, width=3, style="arc")

        title_text = "Welcome!" if is_new else "Welcome Back!"
        sub_text   = "Set your master password to get started." if is_new else "Enter your master password to unlock the vault."

        label(body, title_text, font=FONT_TITLE, fg=WHITE).pack()
        label(body, sub_text, font=FONT_SUB, fg=GREY, wraplength=300).pack(pady=(4, 24))

        label(body, "Master Password", fg=GREY, font=FONT_SMALL).pack(anchor="w")
        pw_row = styled_frame(body)
        pw_row.pack(fill="x", pady=(2, 10))
        pw_entry = entry(pw_row, show="•", width=24)
        pw_entry.pack(side="left", fill="x", expand=True, ipady=8)
        show_var = tk.BooleanVar(value=False)
        def toggle_pw_vis():
            pw_entry.config(show="" if show_var.get() else "•")
        eye_btn = tk.Button(pw_row, text="👁", bg=BG2, fg=GREY,
                            font=FONT_SMALL, relief="flat", bd=0,
                            activebackground=BG2, activeforeground=WHITE,
                            cursor="hand2",
                            command=lambda: [show_var.set(not show_var.get()), toggle_pw_vis()])
        eye_btn.pack(side="left", padx=(4, 0), ipady=8, ipadx=4)
        pw_entry.focus()

        if is_new:
            label(body, "Confirm Password", fg=GREY, font=FONT_SMALL).pack(anchor="w")
            cf_row = styled_frame(body)
            cf_row.pack(fill="x", pady=(2, 16))
            pw_confirm = entry(cf_row, show="•", width=24)
            pw_confirm.pack(side="left", fill="x", expand=True, ipady=8)
            show_var2 = tk.BooleanVar(value=False)
            def toggle_cf_vis():
                pw_confirm.config(show="" if show_var2.get() else "•")
            tk.Button(cf_row, text="👁", bg=BG2, fg=GREY,
                      font=FONT_SMALL, relief="flat", bd=0,
                      activebackground=BG2, activeforeground=WHITE,
                      cursor="hand2",
                      command=lambda: [show_var2.set(not show_var2.get()), toggle_cf_vis()]).pack(side="left", padx=(4,0), ipady=8, ipadx=4)
        else:
            pw_confirm = None

        msg_var = tk.StringVar()
        msg_lbl = label(body, "", fg=RED, font=FONT_SMALL)
        msg_lbl.pack()
        msg_lbl.config(textvariable=msg_var)

        def do_action():
            pw = pw_entry.get()
            if not pw:
                msg_var.set("Please enter a password.")
                return
            if is_new:
                cf = pw_confirm.get()
                if pw != cf:
                    msg_var.set("Passwords don't match!")
                    return
                vault["master_hash"] = hash_master(pw)
                vault["passwords"]   = {}
                save_vault(vault)
                self.master_password = pw
                self.show_dashboard()
            else:
                if vault.get("master_hash") == hash_master(pw):
                    self.master_password = pw
                    self.show_dashboard()
                else:
                    msg_var.set("Incorrect master password.")

        action_text = "Create Vault" if is_new else "Unlock Vault"
        btn(body, action_text, do_action).pack(fill="x", pady=(10, 0))
        pw_entry.bind("<Return>", lambda e: do_action())

    # ══════════════════════════════════════════
    #  SCREEN 2 — DASHBOARD
    # ══════════════════════════════════════════
    def show_dashboard(self):
        self.clear()
        self._center(420, 480)

        self._header("🏠  Dashboard")

        body = styled_frame(self.root, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        vault = load_vault()
        count = len(vault.get("passwords", {}))

        label(body, f"Vault unlocked  ·  {count} password{'s' if count != 1 else ''} stored",
              fg=GREY, font=FONT_SMALL).pack(anchor="w", pady=(0, 20))

        items = [
            ("🔍  Analyse a Password",       self.show_analyse),
            ("⚡  Generate & Save Password", self.show_generate),
            ("📂  View Saved Passwords",     self.show_saved),
        ]

        for text, cmd in items:
            row = tk.Frame(body, bg=BG2, cursor="hand2",
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=5, ipady=12)
            tk.Label(row, text=text, bg=BG2, fg=WHITE,
                     font=FONT_BOLD, padx=16).pack(side="left")
            tk.Label(row, text="›", bg=BG2, fg=MAROON,
                     font=("Segoe UI", 14, "bold")).pack(side="right", padx=16)
            row.bind("<Button-1>", lambda e, c=cmd: c())
            for child in row.winfo_children():
                child.bind("<Button-1>", lambda e, c=cmd: c())
            row.bind("<Enter>", lambda e, r=row: r.config(bg="#222222", highlightbackground=MAROON))
            row.bind("<Leave>", lambda e, r=row: r.config(bg=BG2, highlightbackground=BORDER))

        separator(body).pack(fill="x", pady=20)

        btn(body, "🔒  Lock Vault", self.show_login,
            bg="#1a0000", fg=RED, width=18, pady=6).pack()

    # ══════════════════════════════════════════
    #  SCREEN 3 — ANALYSE
    # ══════════════════════════════════════════
    def show_analyse(self):
        self.clear()
        self._center(440, 580)

        self._header("🔍  Analyse Password", show_back=True, back_cmd=self.show_dashboard)

        body = styled_frame(self.root, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        section_title(body, "Enter Password").pack(anchor="w", pady=(0, 6))
        pw_entry = entry(body, width=32)
        pw_entry.pack(fill="x", ipady=8, pady=(0, 12))

        # ── Strength bar ──────────────────────
        bar_frame = styled_frame(body)
        bar_frame.pack(fill="x", pady=(0, 12))

        bar_top = styled_frame(bar_frame)
        bar_top.pack(fill="x")
        str_label_l = label(bar_top, "Strength", fg=GREY, font=FONT_SMALL)
        str_label_l.pack(side="left")
        str_label_r = label(bar_top, "", fg=GREY, font=FONT_SMALL)
        str_label_r.pack(side="right")

        bar_bg = tk.Frame(body, bg=BG2, height=10)
        bar_bg.pack(fill="x", pady=(4, 0))
        bar_fill = tk.Frame(bar_bg, bg=MAROON, height=10)
        bar_fill.place(x=0, y=0, relheight=1, relwidth=0)

        # ── Feedback area ─────────────────────
        separator(body).pack(fill="x", pady=10)
        section_title(body, "Feedback").pack(anchor="w", pady=(0, 6))

        fb_frame = styled_frame(body)
        fb_frame.pack(fill="x")

        # ── Combinations ──────────────────────
        separator(body).pack(fill="x", pady=10)
        combo_frame = tk.Frame(body, bg=BG2, highlightthickness=1,
                               highlightbackground=BORDER)
        combo_frame.pack(fill="x", ipady=8, ipadx=10)
        label(combo_frame, "Possible Combinations  (NumPy)", fg=GREY, font=FONT_SMALL, bg=BG2).pack(anchor="w", padx=10, pady=(6,0))
        combo_val = label(combo_frame, "—", font=("Segoe UI", 13, "bold"), fg=MAROON, bg=BG2)
        combo_val.pack(anchor="w", padx=10, pady=(0,6))

        def do_analyse(*_):
            pwd = pw_entry.get()
            if not pwd:
                return
            r = analyse_password(pwd)

            # Update bar
            pct = r["score"] / 100
            bar_bg.update_idletasks()
            bar_fill.place(relwidth=pct)
            bar_fill.config(bg=r["color"])
            str_label_r.config(text=f"{r['label']}  {r['score']}%", fg=r["color"])

            # Clear old feedback
            for w in fb_frame.winfo_children():
                w.destroy()

            for kind, msg in r["feedback"]:
                color  = GREEN if kind == "ok" else ORANGE
                symbol = "✓" if kind == "ok" else "⚠"
                row = tk.Frame(fb_frame, bg=("#001a0a" if kind == "ok" else "#1a0a00"),
                               highlightthickness=1,
                               highlightbackground=("#005522" if kind == "ok" else "#553300"))
                row.pack(fill="x", pady=2)
                tk.Label(row, text=f" {symbol}  {msg}", bg=row["bg"],
                         fg=color, font=FONT_SMALL, anchor="w",
                         padx=8, pady=5).pack(fill="x")

            # Combinations via NumPy
            c = r["combinations"]
            if c == float('inf') or c > 1e100:
                combo_val.config(text="> 10¹⁰⁰ combinations")
            else:
                exp = int(np.floor(np.log10(c))) if c > 0 else 0
                mantissa = c / (10 ** exp)
                combo_val.config(text=f"{mantissa:.2f} × 10^{exp}  ({r['charset_size']}^{r['length']})")

        btn(body, "Analyse", do_analyse).pack(fill="x", pady=(14, 0))
        pw_entry.bind("<KeyRelease>", do_analyse)

    # ══════════════════════════════════════════
    #  SCREEN 4 — GENERATE & SAVE
    # ══════════════════════════════════════════
    def show_generate(self):
        self.clear()
        self._center(440, 580)

        self._header("⚡  Generate & Save", show_back=True, back_cmd=self.show_dashboard)

        body = styled_frame(self.root, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        section_title(body, "App Name").pack(anchor="w", pady=(0, 6))
        app_entry = entry(body, width=32)
        app_entry.pack(fill="x", ipady=8, pady=(0, 14))

        section_title(body, "Password Length").pack(anchor="w", pady=(0, 6))
        len_frame = styled_frame(body)
        len_frame.pack(fill="x", pady=(0, 14))
        len_var = tk.IntVar(value=16)
        len_lbl = label(len_frame, "16", font=FONT_BOLD, fg=MAROON)
        len_lbl.pack(side="right")
        slider = ttk.Scale(len_frame, from_=8, to=32, orient="horizontal",
                           variable=len_var,
                           command=lambda v: len_lbl.config(text=str(int(float(v)))))
        slider.pack(side="left", fill="x", expand=True)

        outline_btn(body, "⚡  Generate Password", lambda: do_generate()).pack(fill="x", pady=(0, 10))

        # Generated password display
        gen_frame = tk.Frame(body, bg=BG2, highlightthickness=1,
                             highlightbackground=MAROON)
        gen_frame.pack(fill="x", ipady=10)
        gen_var = tk.StringVar(value="Click Generate to create a password")
        gen_lbl = tk.Label(gen_frame, textvariable=gen_var, bg=BG2, fg=GREY,
                           font=FONT_MONO, wraplength=340)
        gen_lbl.pack(padx=10, pady=6)

        # Strength mini bar
        bar_frame = styled_frame(body)
        bar_frame.pack(fill="x", pady=(8, 0))
        str_lbl = label(bar_frame, "", fg=GREY, font=FONT_SMALL)
        str_lbl.pack(side="right")
        label(bar_frame, "Strength", fg=GREY, font=FONT_SMALL).pack(side="left")

        mini_bg   = tk.Frame(body, bg=BG2, height=7)
        mini_bg.pack(fill="x", pady=(3, 10))
        mini_fill = tk.Frame(mini_bg, bg=GREEN, height=7)
        mini_fill.place(x=0, y=0, relheight=1, relwidth=0)

        history_lbl = label(body, "", fg=GREY, font=FONT_SMALL)
        history_lbl.pack(anchor="w")

        save_btn = btn(body, "💾  Save Encrypted", lambda: do_save())
        save_btn.pack(fill="x", pady=(10, 0))
        save_btn.config(state="disabled", bg=BORDER)

        generated_pw = {"value": None}

        def do_generate():
            length = int(len_var.get())
            pwd = generate_password(length)
            generated_pw["value"] = pwd
            gen_var.set(pwd)
            gen_lbl.config(fg=WHITE)

            r = analyse_password(pwd)
            mini_fill.place(relwidth=r["score"] / 100)
            mini_fill.config(bg=r["color"])
            str_lbl.config(text=f"{r['label']}  {r['score']}%", fg=r["color"])

            # Check history
            vault = load_vault()
            app = app_entry.get().strip()
            if app and app in vault.get("passwords", {}):
                hist = vault["passwords"][app].get("history", [])
                for h in hist:
                    try:
                        if decrypt_password(h, self.master_password) == pwd:
                            history_lbl.config(text="⚠ Matches a recent password — regenerating...", fg=ORANGE)
                            do_generate()
                            return
                    except Exception:
                        pass
                history_lbl.config(text="✓ Not in last 5 passwords", fg=GREEN)
            else:
                history_lbl.config(text="✓ Ready to save", fg=GREEN)

            save_btn.config(state="normal", bg=MAROON)

        def do_save():
            app = app_entry.get().strip()
            pwd = generated_pw["value"]
            if not app:
                messagebox.showwarning("App Name", "Please enter an app name.")
                return
            if not pwd:
                messagebox.showwarning("No Password", "Generate a password first.")
                return

            vault = load_vault()
            passwords = vault.get("passwords", {})

            enc_pwd  = encrypt_password(pwd, self.master_password)
            existing = passwords.get(app, {})
            history  = existing.get("history", [])

            # Keep only last 4 (+ new = 5 total)
            if existing.get("encrypted_password"):
                history.append(existing["encrypted_password"])
            history = history[-4:]

            passwords[app] = {
                "encrypted_password": enc_pwd,
                "saved_on": str(date.today()),
                "history": history
            }
            vault["passwords"] = passwords
            save_vault(vault)

            messagebox.showinfo("Saved!", f"Password for '{app}' saved securely! 🔒")
            self.show_dashboard()

    # ══════════════════════════════════════════
    #  SCREEN 5 — VIEW SAVED
    # ══════════════════════════════════════════
    def show_saved(self):
        self.clear()
        self._center(440, 560)

        self._header("📂  Saved Passwords", show_back=True, back_cmd=self.show_dashboard)

        vault    = load_vault()
        passwords = vault.get("passwords", {})

        body = styled_frame(self.root, padx=24, pady=16)
        body.pack(fill="both", expand=True)

        if not passwords:
            label(body, "No passwords saved yet.", fg=GREY, font=FONT_BODY).pack(pady=40)
            btn(body, "Go Generate One", self.show_generate).pack()
            return

        label(body, f"{len(passwords)} password(s) saved  ·  encrypted with Fernet",
              fg=GREY, font=FONT_SMALL).pack(anchor="w", pady=(0, 12))

        canvas = tk.Canvas(body, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
        scroll_frame = styled_frame(canvas)

        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for app_name, data in passwords.items():
            card = tk.Frame(scroll_frame, bg=BG2, highlightthickness=1,
                            highlightbackground=BORDER)
            card.pack(fill="x", pady=5, ipadx=10, ipady=8)

            # Avatar
            initials = "".join(w[0].upper() for w in app_name.split()[:2])
            av = tk.Frame(card, bg=MAROON, width=36, height=36)
            av.pack(side="left", padx=(10, 0))
            av.pack_propagate(False)
            tk.Label(av, text=initials[:2], bg=MAROON, fg=WHITE,
                     font=("Segoe UI", 9, "bold")).place(relx=0.5, rely=0.5, anchor="center")

            info = styled_frame(card, bg=BG2)
            info.pack(side="left", padx=10, fill="x", expand=True)
            label(info, app_name, font=FONT_BOLD, fg=WHITE, bg=BG2).pack(anchor="w")
            label(info, f"Saved: {data.get('saved_on','—')}  ·  ••••••••••••",
                  fg=GREY, font=FONT_SMALL, bg=BG2).pack(anchor="w")

            # Decrypt button
            revealed = {"shown": False}
            reveal_frame = styled_frame(card, bg=BG2)
            reveal_frame.pack(side="right", padx=10)

            def make_toggle(af=reveal_frame, an=app_name, d=data, rv=revealed, card_ref=card):
                pw_lbl = tk.Label(af, text="", bg=BG2, fg=WHITE,
                                  font=("Courier New", 9), wraplength=120)

                def toggle():
                    if not rv["shown"]:
                        try:
                            plain = decrypt_password(d["encrypted_password"], self.master_password)
                            pw_lbl.config(text=plain, fg=GREEN)
                            pw_lbl.pack(pady=(0, 2))
                            toggle_b.config(text="Hide", bg=BG2)
                            rv["shown"] = True
                        except Exception:
                            pw_lbl.config(text="Decryption error", fg=RED)
                            pw_lbl.pack()
                    else:
                        pw_lbl.pack_forget()
                        toggle_b.config(text="Show", bg=BG2)
                        rv["shown"] = False

                def do_delete():
                    if messagebox.askyesno("Delete", f"Delete password for '{an}'?\nThis cannot be undone."):
                        v = load_vault()
                        v.get("passwords", {}).pop(an, None)
                        save_vault(v)
                        card_ref.destroy()

                toggle_b = tk.Button(af, text="Show", bg=BG2, fg=MAROON,
                                     font=FONT_SMALL, relief="flat", bd=0,
                                     highlightthickness=1, highlightbackground=MAROON,
                                     cursor="hand2", command=toggle, padx=8, pady=3)
                toggle_b.pack(pady=(0, 4))

                del_b = tk.Button(af, text="Delete", bg=BG2, fg=RED,
                                  font=FONT_SMALL, relief="flat", bd=0,
                                  highlightthickness=1, highlightbackground=RED,
                                  cursor="hand2", command=do_delete, padx=6, pady=3)
                del_b.pack()
                return toggle_b

            make_toggle()

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = PasswordVaultApp(root)
    root.mainloop()