import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class DataManager:

    USERS_FILE = os.path.join(BASE_DIR, "static/data", "users.json")
    LOGIN_LOG_FILE = os.path.join(BASE_DIR, "static/data", "logins.json")
    
    head_folder = 'static/data'
    files_names = [
        'users',
        'logins'
    ]

    @staticmethod
    def load_json(file_name):
        if file_name not in DataManager.files_names:
            return None
        file_path = os.path.join(BASE_DIR, DataManager.head_folder, file_name + ".json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


    @staticmethod
    def save_json(file_name, data):
        if file_name not in DataManager.files_names:
            return None
        file_path = os.path.join(BASE_DIR, DataManager.head_folder, file_name + ".json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


    @staticmethod
    def get_user_cases(username):
        safe_name = username.replace(" ", "_")
        folder_path = os.path.join(DataManager.head_folder, safe_name)
        file_path = os.path.join(folder_path, f"{safe_name}_cases.json")

        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_user_case(username, case_data):
        safe_name = username.replace(" ", "_")
        folder_path = os.path.join(DataManager.head_folder, safe_name)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{safe_name}_cases.json")

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                cases = json.load(f)
                cases.append(case_data)

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(cases, f, indent=2, ensure_ascii=False)

        