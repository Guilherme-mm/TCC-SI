from ..collections.MongoCollection import MongoCollection
from ...exception.MongoNoDiferencesFoundException import MongoNoDiferencesFoundException

class ConfigurationsManager():
    def __init__(self):
        self.__mongoCollection = MongoCollection()
        self.__mongoCollection.selectCollection("configurations")

    def setConfiguration(self, key, value) -> dict:
        configDict = {
            "key": key,
            "value": value
        }

        queryFilter = {
            "key":key
        }

        result = self.__mongoCollection.update(document=configDict, queryFilter=queryFilter, upsert=True)
        
        return result
        # if result["matched_count"] > 0:
        #     if result["updated_count"] == 0 or result["upserted_count"] == 0:
        #         raise MongoNoDiferencesFoundException()
        #     else:
        #         return True
        # else:
        #     if result["upserted_count"] > 0:
        #         return True
