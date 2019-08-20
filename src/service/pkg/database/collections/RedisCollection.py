import redis # pylint: disable=import-error
from .Collection import Collection

class RedisCollection(Collection):
    def __init__(self):
        self.__redis = redis.Redis(host="redis", port=6379,db=0)

    def get(self, key:str) -> str:
        result = self.__redis.get(key)
        return result.decode('utf-8')

    def insert(self, key:str, value:str) -> bool:
        result = self.__redis.set(key, value)
        return result
