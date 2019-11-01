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

        closestNeighbors = simGraphManager.getByWeight(actorId=actorId, limit=quantity)
        neighborsIds = []

        for neighbor in closestNeighbors:
            neighborsIds.append(neighbor["node"]["actorId"])

        #Getting the objects that the actor interacted
        actorData = cliendDataStorage.getActorData(actorId)
        actorVectorData = actorData["dataVector"]

        #Getting object data from neighbors
        neighborsData = cliendDataStorage.getActorsData(neighborsIds)

        objectList = []
        recommendations = []

        for neighbor in closestNeighbors:
            neighborId = neighbor["node"]["actorId"]
            relationshipWeight = neighbor["relationship"]["weight"]

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
                        objectData["weightedValue"] = float(objectData["value"]) * relationshipWeight
                        objectList.append(objectData)
                        # recommendations.append(objectData["objectId"])

                    # if len(recommendations) == quantity:
                    #     break

                # if len(recommendations) == quantity:
                #     break

            # if len(recommendations) == quantity:
            #     break

        recommendations = objectList
        recommendations.sort(key=lambda x: x["weightedValue"],reverse=True)
        return recommendations[:quantity]
