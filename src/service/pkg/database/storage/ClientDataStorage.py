from ..collections.MongoCollection import MongoCollection
from ...utils.ClientCommunicationUtils import ClientCommunicationUtils

class ClientDataStorage():
    def __init__(self):
        self.__mongoCollection = MongoCollection()
        self.__mongoCollection.selectCollection("client_data")

    def saveClientData(self, clientData, dataMap):
        ClientCommunicationUtils.sendMessage("Persisting raw data")

        itensCount = len(clientData.values())
        itensCounter = 0
        for actorId, dataVector in clientData.items():
            itensCounter = itensCounter + 1
            sanitizedDataVector = []
            for objectId, objectIndex in dataMap.items():
                if dataVector[objectIndex] == 0:
                    continue

                sanitizedDataVector.append({"objectId": objectId, "value":dataVector[objectIndex]})

            acorDict = {
                "actorId": actorId,
                "dataVector": sanitizedDataVector
            }

            queryFilter = {
                "actorId":actorId
            }

            self.__mongoCollection.update(document=acorDict, queryFilter=queryFilter, upsert=True)
            ClientCommunicationUtils.sendProgress((itensCounter * 100)/itensCount)

    def getActorData(self, actorId):
        queryFilter = {
            "actorId":actorId
        }

        return self.__mongoCollection.get(queryFilter)

    def getActorsData(self, actorsIds):
        assert isinstance(actorsIds, list)

        queryFilter = {
            "actorId":{"$in":actorsIds}
        }

        return self.__mongoCollection.all(queryFilter)

    def deleteClientData(self):
        return self.__mongoCollection.wipeSelectedCollectionData()
