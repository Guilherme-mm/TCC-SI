from ..collections.Neo4JCollection import Neo4JCollection

class SimilarityGraphManager():
    def __init__(self):
        self.__neo4jCollection = Neo4JCollection()
        print("Connection with database granted")

    def generateGraphFromSimMatrix(self, similarityMatrix, rowActorsMap):
        labels = ["Actor"]
        properties = {}

        #Adding the actors nodes
        print("Creating nodes...")
        for actorRow, actorId in rowActorsMap.items():
            properties["actorId"] = actorId
            try:
                self.__neo4jCollection.insert(labels, properties)
                print("Actor {} created".format(actorId))
            except Exception:
                print("Actor {} skipped".format(actorId))
                continue

        #Creating the relationships based on the matrix
        print("Creating the relationships")
        for rowIdx, row in enumerate(similarityMatrix):
            rowActorId = rowActorsMap[rowIdx]
            print("Creating relationships for {}".format(rowActorId))
            for columnIdx, relationshipWeight in enumerate(row):
                columnActorId = rowActorsMap[columnIdx]
                if relationshipWeight > 0:
                    self.__neo4jCollection.createRelationship(labels, rowActorId, labels, columnActorId, relationshipWeight)

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
