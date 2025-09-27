import os
import json
from werkzeug.utils import secure_filename

# נתיבים מרכזיים
PTAH_LAWOFFICE      = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # LawOffice
PTAH_APP            = os.path.join(PTAH_LAWOFFICE, "app")                                   # LawOffice/app
BASE_DATA           = os.path.join(PTAH_APP, "data")                                        # LawOffice/app/data
BASE_INDEXS         = os.path.join(BASE_DATA, "indexs")                                     # LawOffice/app/data/indexs


class DataManager:

    system_files = ["users", "logins"]

    @staticmethod
    def load_json_from_path(path, file_name, on_fail_return = None):

        file_path = os.path.join(path, f"{file_name}.json")
        if not os.path.exists(file_path):
            return on_fail_return

        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                print('Error from data managment')
                return on_fail_return

    @staticmethod
    def load_json_from_data(file_name, on_fail_return = None):
        return DataManager.load_json_from_path(BASE_DATA, file_name, on_fail_return)
    
    @staticmethod
    def load_json_from_data_indexs(file_name, on_fail_return = None):
        return DataManager.load_json_from_path(BASE_INDEXS, file_name, on_fail_return)
    
    @staticmethod
    def save_json_to_path(path, file_name, data):
        file_path = os.path.join(path, f"{file_name}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    @staticmethod
    def save_json_to_data(file_name, data):
        DataManager.save_json_to_path(BASE_DATA, file_name, data)

    @staticmethod
    def save_json_to_data_indexs(file_name, data):
        DataManager.save_json_to_path(BASE_INDEXS, file_name, data)