import json


class Database:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'r+', encoding='utf-8') as f:
            self.table = json.load(f)

    def commit(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.table, f, indent='\t')


db = Database("db.json")
