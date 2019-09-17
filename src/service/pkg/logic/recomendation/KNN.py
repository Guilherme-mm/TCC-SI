from .SelectionAlgorithm import SelectionAlgorithm
from ...database.storage.SimilarityGraphManager import SimilarityGraphManager
from ...database.storage.ClientDataStorage import ClientDataStorage

class KNN(SelectionAlgorithm):
    def __init__(self):
        pass

    def getRecommendations(self, actorId:str, quantity:int=10):
        assert actorId
        assert isinstance(quantity, int)

        simGraphManager =  SimilarityGraphManager()
        cliendDataStorage = ClientDataStorage()

        closestNeighbors = simGraphManager.getByWeight(actorId=actorId)
        neighborsIds = []

        for neighbor in closestNeighbors:
            neighborsIds.append(neighbor["node"]["actorId"])


        #Getting the objects that the actor interacted
        actorData = cliendDataStorage.getActorData(actorId)
        actorVectorData = actorData["dataVector"]

        #Getting object data from neighbors
        neighborsData = cliendDataStorage.getActorsData(neighborsIds)

        recommendations = []

        for neighbor in closestNeighbors:
            neighborId = neighbor["node"]["actorId"]

            for neighborData in neighborsData:
                if neighborData["actorId"] != neighborId:
                    continue

                neighborVectorData = neighborData["dataVector"]
                for objectData in neighborVectorData:
                    objectNotUsedByActor = True

                    for actorObjectData in actorVectorData:
                        if actorObjectData["objectId"] == objectData["objectId"]:
                            objectNotUsedByActor = False

                    if objectNotUsedByActor:
                        recommendations.append(objectData["objectId"])
                    
                    if len(recommendations) == quantity:
                        break

                if len(recommendations) == quantity:
                    break

            if len(recommendations) == quantity:
                break

        return recommendations
