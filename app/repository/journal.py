import random
import pymongo
from pymongo.collection import ObjectId
from pyramid.request import Request
from bson import ObjectId


class JournalRepository:
    def __init__(self, request: Request):
        self.db = request.registry.db["journal"]
        self.collection = self.db["journal"]

        self.collection.create_index(
            [
                ("title", pymongo.TEXT),
                ("short_summary", pymongo.TEXT),
                ("content", pymongo.TEXT),
                ("abbreviation", pymongo.TEXT),
            ]
        )

    def create_journal(self, journal):
        result = self.collection.insert_one(journal)
        return str(result.inserted_id)

    def find_by_id(self, journal_id):
        journal = self.collection.find_one({"_id": ObjectId(journal_id)})
        if journal:
            journal["_id"] = str(journal["_id"])
        return journal

    def find_all_journals(self):
        journals = list(self.collection.find({}))
        for journal in journals:
            journal["_id"] = str(journal["_id"])

        random.shuffle(journals)

        return journals

    def update_journal(self, journal_id, updates):
        self.collection.update_one({"_id": ObjectId(journal_id)}, {"$set": updates})

    def delete_journal(self, journal_id):
        self.collection.delete_one({"_id": ObjectId(journal_id)})
