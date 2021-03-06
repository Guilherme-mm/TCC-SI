from ..collections.Neo4JCollection import Neo4JCollection
from ...utils.ClientCommunicationUtils import ClientCommunicationUtils

class SimilarityGraphManager():
    def __init__(self):
        self.__neo4jCollection = Neo4JCollection()
        # print("Connection with database granted")

    def generateGraphFromSimMatrix(self, similarityMatrix, rowActorsMap):
        labels = ["Actor"]
        properties = {}

        #Adding the actors nodes
        ClientCommunicationUtils.sendMessage("Creating nodes")
        actorsCount = len(rowActorsMap.values())
        actorsCounter = 0

        for actorRow, actorId in rowActorsMap.items(): # pylint: disable=unused-variable
            actorsCounter = actorsCounter + 1
            properties["actorId"] = actorId
            try:
                self.__neo4jCollection.insert(labels, properties)
            except Exception: # pylint: disable=broad-except
                print("Actor {} skipped".format(actorId))
            finally:
                ClientCommunicationUtils.sendProgress((actorsCounter * 100)/actorsCount)

        #Creating the relationships based on the matrix
        ClientCommunicationUtils.sendMessage("Connecting nodes")
        rowsCount = len(similarityMatrix)
        rowsCounter = 0
        for rowIdx, row in enumerate(similarityMatrix):
            rowsCounter = rowsCounter + 1
            rowActorId = rowActorsMap[rowIdx]

            print("Creating relationships for {}".format(rowActorId))
            for columnIdx, relationshipWeight in enumerate(row):
                columnActorId = rowActorsMap[columnIdx]
                if relationshipWeight != 0:
                    self.__neo4jCollection.createRelationship(labels, rowActorId, labels, columnActorId, relationshipWeight)

            ClientCommunicationUtils.sendProgress((rowsCounter *100)/rowsCount)

        return True

    def getByWeight(self, actorId:str, order:str="desc", limit:int=10):
        orderBy = {
            "direction":order,
            "properties":[
                {
                    "element":"r",
                    "property":"weight"
                }
            ]
        }
        nodeLabels= ["Actor"]
        relationshipLabels = ["SIMILAR"]
        node1Properties = {"actorId":actorId}

        results = self.__neo4jCollection.get(nodeALabels=nodeLabels, nodeAProperties=node1Properties, relationshipLabels=relationshipLabels, nodeBLabels=nodeLabels, orderBy=orderBy, limit=limit)
        return results

    def clearGraph(self):
        result = self.__neo4jCollection.truncateDB()
        return result
