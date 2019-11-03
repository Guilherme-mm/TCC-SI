from .SelectionAlgorithm import SelectionAlgorithm
from ...database.storage.SimilarityGraphManager import SimilarityGraphManager
from ...database.storage.ClientDataStorage import ClientDataStorage

class KNN(SelectionAlgorithm):
    def __init__(self):
        pass

    def getRecommendations(self, actorId:str, quantity:int=10, K:int=5):
        assert actorId
        assert isinstance(quantity, int)

        simGraphManager =  SimilarityGraphManager()
        cliendDataStorage = ClientDataStorage()

        closestNeighbors = simGraphManager.getByWeight(actorId=actorId, limit=K)
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

        # For each neighbor of the actor...
        for neighbor in closestNeighbors:
            neighborId = neighbor["node"]["actorId"]
            relationshipWeight = neighbor["relationship"]["weight"]

            # Iterates over de neighbors data array
            for neighborData in neighborsData:
                # Only proceeds when encounters the current neighbor data
                if neighborData["actorId"] != neighborId:
                    continue

                neighborVectorData = neighborData["dataVector"]

                # For each object in the current neighbor data...
                for objectData in neighborVectorData:
                    objectNotUsedByActor = True

                    # Iterates over the list of objects of the actor
                    for actorObjectData in actorVectorData:
                        if actorObjectData["objectId"] == objectData["objectId"]:
                            objectNotUsedByActor = False

                    if objectNotUsedByActor:
                        objectData["weightedValue"] = float(objectData["value"]) * relationshipWeight
                        objectList.append(objectData)

        recommendations = objectList
        recommendations.sort(key=lambda x: x["weightedValue"],reverse=True)
        return recommendations[:quantity]
