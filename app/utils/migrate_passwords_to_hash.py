#!/usr/bin/env python3
"""
הרצה חד-פעמית:
python migrate_passwords_to_hash.py
• יוצר גיבוי users.json.bak
• מחליף סיסמאות גלויות ב-hash
• משאיר רשומות שכבר בהאש כמו שהן
"""
import os, json, shutil
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
USERS_FILE = os.path.join(BASE_DIR, "static", "data", "users.json")
BACKUP     = USERS_FILE + ".bak"

def is_hashed(pwd: str) -> bool:
    """אם הסטרינג כבר נראה כמו werkzeug hash‏"""
    return pwd.startswith("pbkdf2:") or pwd.startswith("scrypt:")

def main():
    if not os.path.exists(USERS_FILE):
        print("❌ users.json לא נמצא")
        return

    # גיבוי
    if not os.path.exists(BACKUP):
        shutil.copy2(USERS_FILE, BACKUP)
        print(f"✔ גיבוי נשמר: {BACKUP}")

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    changed = 0
    for u in users:
        pwd = u.get("password", "")
        if not is_hashed(pwd):
            u["password"] = generate_password_hash(pwd.strip())
            changed += 1

    if changed:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print(f"✔ הומרו {changed} סיסמאות")
    else:
        print("⏩ אין סיסמאות גלויות – אין מה להמיר")

if __name__ == "__main__":
    main()
