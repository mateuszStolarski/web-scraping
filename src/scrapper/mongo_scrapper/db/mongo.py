from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDataBase:
    def __init__(self, connection_string: str) -> None:
        self.client = MongoClient(connection_string)
        self._databse = self.client["scrapper"]

    def get_collection(self, name: str) -> Collection:
        return self._databse[name]
