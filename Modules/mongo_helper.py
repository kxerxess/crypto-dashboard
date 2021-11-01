import pymongo
import urllib

from pymongo.message import query


class Mongo:
    def __init__(self, mongo_settings) -> None:
        host = mongo_settings["host"]
        port = mongo_settings["port"]
        username = mongo_settings["username"]
        password = mongo_settings["password"]
        db = mongo_settings["db"]
        connection_string = (
            "mongodb+srv://"
            + username
            + ":"
            + urllib.parse.quote(password)
            + "@"
            + host
            + "/"
            + db
            + "?retryWrites=true&w=majority"
        )
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db]
        self.user = self.db.user
        self.data = self.db.data
        self.app = self.db.app
        self.symbols = self.db.symbols

    def get_all_symbols(self):
        return self.symbols.find({})

    def get_target_symbols(self):
        return self.symbols.find({"target": True})

    def update_target_status(self, name, status):
        query = {
            "name": name,
        }
        data = {
            "$set": {
                "target": status,
            },
        }
        try:
            self.symbols.update_one(query, data)
            return True
        except:
            return False

    def update_symbol_sync(self, symbol, frame, ts):
        query = {
            "symbol": symbol,
        }
        data = {
            "$set": {
                frame: ts,
            },
        }
        self.symbols.update_one(query, data)
