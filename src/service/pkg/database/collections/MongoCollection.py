from pymongo import MongoClient # pylint: disable=import-error
from .Collection import Collection

class MongoCollection(Collection):
    def __init__(self):
        self.__collection = None
        self.__connection = MongoClient('mongo', 27017)
        self.__database = self.__connection.GERT

    def selectCollection(self, collectionName:str):
        self.__collection = self.__database[collectionName]

    def insert(self, document:dict):
        insertedDocumentsCount = self.__collection.insert_one(document).inserted_count

        if insertedDocumentsCount > 0:
            return True
        else:
            return False

    def update(self, document:dict, queryFilter:dict, upsert:bool=False) -> dict:
        updateResult = self.__collection.update_one(queryFilter, {'$set': document}, upsert=upsert)
        try:
            updateCount = updateResult.modified_count
        except AttributeError:
            updateCount = 0

        try:
            upsertCount = updateResult.upserted_count
        except AttributeError:
            upsertCount = 0

        try:
            matchedCount = updateResult.matchedCount
        except AttributeError:
            matchedCount = 0

        return {
            "upserted_count":upsertCount,
            "updated_count":updateCount,
            "matched_count": matchedCount
        }

    def get(self, queryFilter:dict):
        return self.__collection.find_one(queryFilter)

    def all(self, queryFilter:dict):
        docs = []
        cursor = self.__collection.find(queryFilter)
        for doc in cursor:
            docs.append(doc)

        return docs
