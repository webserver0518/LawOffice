# user_managment.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.data_managment import DataManager


class UserManager:

    # ---------- עזר ----------
    @classmethod
    def _now(cls):
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    # ---------- CRUD משתמשים ----------
    @classmethod
    def load_users(cls):
        return DataManager.load_json_from_data("users") or []

    @classmethod
    def save_users(cls, users):
        DataManager.save_json_to_data("users", users)

    @classmethod
    def add_user(cls, username: str, password: str) -> bool:
        users = cls.load_users()
        if any(u["username"] == username for u in users):
            return False
        users.append({
            "username": username.strip(),
            "password": generate_password_hash(password.strip()),
            "created_at": cls._now()
        })
        cls.save_users(users)
        return True

    @classmethod
    def update_password(cls, username: str, new_password: str) -> None:
        users = cls.load_users()
        for user in users:
            if user["username"] == username:
                user["password"] = generate_password_hash(new_password.strip())
        cls.save_users(users)

    @classmethod
    def delete_user(cls, username: str) -> None:
        if username == "admin":
            return
        users = [u for u in cls.load_users() if u["username"] != username]
        cls.save_users(users)
        logins = cls.load_logins()
        logins.pop(username, None)
        cls.save_logins(logins)

    # ---------- אימות ----------
    @classmethod
    def authenticate(cls, username: str, password: str) -> str:
        for user in cls.load_users():
            if user["username"] == username.strip():
                if check_password_hash(user["password"], password.strip()):
                    return "success"
                return "wrong_password"
        return "user_not_found"

    # ---------- לוג-אין / לוג-אאוט ----------
    @classmethod
    def load_logins(cls):
        return DataManager.load_json_from_data("logins") or {}

    @classmethod
    def save_logins(cls, logins):
        DataManager.save_json_to_data("logins", logins)

    @classmethod
    def record_login(cls, username: str, session_id: str):
        logins = cls.load_logins()
        logins.setdefault(username, []).append({
            "session_id": session_id,
            "login": cls._now()
        })
        cls.save_logins(logins)

    @classmethod
    def record_logout(cls, username: str, session_id: str):
        logins = cls.load_logins()
        sessions = logins.get(username, [])
        for sess in sessions[::-1]:                 # חפש מהסוף
            if sess.get("session_id") == session_id:
                sess["logout"] = cls._now()
                break
        cls.save_logins(logins)
