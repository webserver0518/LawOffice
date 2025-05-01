import os
import json
from werkzeug.utils import secure_filename

# נתיבים מרכזיים
PTAH_LAWOFFICE      = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # LawOffice
PTAH_APP            = os.path.join(PTAH_LAWOFFICE, "app")                                   # LawOffice/app
BASE_DATA           = os.path.join(PTAH_APP, "data")                                        # LawOffice/app/data
BASE_UPLOADS        = os.path.join(PTAH_LAWOFFICE, "uploads")                               # LawOffice/uploads

print(PTAH_LAWOFFICE)
print(PTAH_APP)
print(BASE_DATA)
print(BASE_UPLOADS)


class DataManager:

    system_files = ["users", "logins"]

    @staticmethod
    def load_json(file_name):

        file_path = os.path.join(BASE_DATA, f"{file_name}.json")
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
            
    @staticmethod
    def save_json(file_name, data):
       
        file_path = os.path.join(BASE_DATA, f"{file_name}.json")

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def get_user_cases(username):
        safe_name = secure_filename(username)
        return DataManager.load_json("cases_index") or []

    @staticmethod
    def save_case_with_sequence(username, case_data):
        safe_name = secure_filename(username)
        user_dir = os.path.join(BASE_UPLOADS, safe_name)
        print('safe_name: ' + safe_name)
        print('user_dir: ' + user_dir)
        print('case_data: ' + str(case_data))
        
        os.makedirs(user_dir, exist_ok=True)
        """
        index_path = os.path.join(user_dir, "cases_index.json")
        cases_index = []

        # טען את קובץ האינדקס אם קיים
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                try:
                    cases_index = json.load(f)
                except json.JSONDecodeError:
                    cases_index = []

        # מספר סידורי חדש
        case_number = len(cases_index) + 1
        folder_name = f"תיק_{case_number:04d}"

        case_data["serial_number"] = case_number
        case_data["folder_name"] = folder_name

        # צור תיקייה לתיק
        case_dir = os.path.join(user_dir, folder_name)
        os.makedirs(case_dir, exist_ok=True)

        # שמור את הקובץ הראשי של התיק
        case_json_path = os.path.join(case_dir, "case.json")
        with open(case_json_path, 'w', encoding='utf-8') as f:
            json.dump(case_data, f, ensure_ascii=False, indent=2)

        # הוסף לאינדקס
        cases_index.append({
            "serial_number": case_number,
            "folder_name": folder_name,
            "case_title": case_data.get("case_title"),
            "client_name": case_data.get("client_name"),
            "category": case_data.get("category"),
            "date": case_data.get("date")
        })

        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(cases_index, f, ensure_ascii=False, indent=2)
        """