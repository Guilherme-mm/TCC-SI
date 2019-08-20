from ..collections.RedisCollection import RedisCollection
from ..collections.MongoCollection import MongoCollection

class ConfigurationsManager():
    def __init__(self):
        self.__redisCollection = RedisCollection()
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

        resultMongo = self.__mongoCollection.update(document=configDict, queryFilter=queryFilter, upsert=True)
        resultRedis = self.__redisCollection.insert(key=configDict["key"], value=configDict["value"])

        mergedResult = {
            "inserted":resultMongo["upserted_count"],
            "updated":resultMongo["updated_count"],
            "matched":resultMongo["matched_count"],
            "cached_in_memory":resultRedis
        }

        return mergedResult

    def getConfiguration(self, key:str) -> str:
        #first searches the configuration on the in memory db
        result = self.__redisCollection.get(key)

        #if not found in memory, look up on mongodb
        # if result is None:
            # queryFilter = {
            #     "key":key
            # }

            # result = self.__mongoCollection.find_one(queryFilter=queryFilter)

        return result
