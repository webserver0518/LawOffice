import os
import json
from datetime import datetime, timezone


class Config:
    SECRET_KEY = 'secret'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'youremail@gmail.com'
    MAIL_PASSWORD = 'yourpassword'
    BASE_DIR = 'users/israel_1234'


class GreetingHelper:
    @staticmethod
    def get_greeting():
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "בוקר טוב"
        elif 12 <= hour < 17:
            return "צהריים טובים"
        elif 17 <= hour < 22:
            return "ערב טוב"
        else:
            return "לילה טוב"

    @staticmethod
    def get_current_time():
        return datetime.now().strftime('%H:%M')


class CaseManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.data_file = os.path.join(base_dir, 'data', 'cases.json')
        self.docs_file = os.path.join(base_dir, 'data', 'documents.json')
        self.counter_file = os.path.join(base_dir, 'data', 'case_counter.txt')
        self.cases_dir = os.path.join(base_dir, 'cases')
        os.makedirs(self.cases_dir, exist_ok=True)
        os.makedirs(os.path.join(base_dir, 'data'), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def load_cases(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_cases(self, cases):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f, ensure_ascii=False, indent=2)

    def get_next_case_id(self):
        if not os.path.exists(self.counter_file):
            with open(self.counter_file, 'w', encoding='utf-8') as f:
                f.write('1')
        with open(self.counter_file, 'r+', encoding='utf-8') as f:
            current = int(f.read().strip() or 1)
            new_id = f"{current:04d}"
            f.seek(0)
            f.truncate()
            f.write(str(current + 1))
        return new_id

    def create_case(self, data):
        cases = self.load_cases()
        cases.append(data)
        self.save_cases(cases)


class DocumentManager:
    def __init__(self, docs_file):
        self.docs_file = docs_file
        if not os.path.exists(docs_file):
            with open(docs_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_documents(self):
        with open(self.docs_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_documents(self, docs):
        with open(self.docs_file, 'w', encoding='utf-8') as f:
            json.dump(docs, f, ensure_ascii=False, indent=2)

    def add_document(self, document):
        docs = self.load_documents()
        docs.append(document)
        self.save_documents(docs)

    def delete_document(self, case_id, folder, filename):
        docs = self.load_documents()
        docs = [d for d in docs if not (
            d['case_id'] == case_id and 
            d['folder'] == folder and 
            d['filename'] == filename
        )]
        self.save_documents(docs)

