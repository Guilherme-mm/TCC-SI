from neo4j import GraphDatabase # pylint: disable=import-error
from .Collection import Collection

class Neo4JCollection(Collection):
    def __init__(self):
        print("Getting neo4j connection")
        self.__driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "gertneo4j"))

    def insert(self, labels, properties):
        with self.__driver.session() as session:
            assert isinstance(labels, list) and labels
            assert isinstance(properties, dict)

            labelsString = ":".join(labels)
            cypherQuery = "CREATE (a:"+labelsString+" {properties})"
            session.run(statement=cypherQuery, properties=properties)
            session.close()

    def createRelationship(self, nodeALabels, nodeAId, nodeBLabels, nodeBId, relationshipWeight=1, idProperty="actorId"):
        with self.__driver.session() as session:
            assert isinstance(nodeALabels, list) and nodeALabels
            assert isinstance(nodeBLabels, list) and nodeBLabels

            labelDelimiter = ':'
            nodeALabelsString = labelDelimiter.join(nodeALabels)
            nodeBLabelsString = labelDelimiter.join(nodeBLabels)

            cypherQuery = "MATCH (a:"+nodeALabelsString+"),(b:"+nodeBLabelsString+")"
            cypherQuery = cypherQuery+" WHERE a."+str(idProperty)+"='"+str(nodeAId)+"' AND b."+str(idProperty)+"='"+str(nodeBId)+"'"
            cypherQuery = cypherQuery+" CREATE (a)-[r:SIMILAR {weight: "+str(relationshipWeight)+"}]->(b)"
            session.run(statement=cypherQuery)
            session.close()

    def get(self, nodeALabels, nodeAProperties, relationshipLabels, nodeBLabels, orderBy, limit):
        with self.__driver.session() as session:
            nodeALabelsString = ":".join(nodeALabels)
            nodeBLabelsString = ":".join(nodeBLabels)
            relationshipLabelsString = ":".join(relationshipLabels)

            orderString = ""
            if isinstance(orderBy, dict):
                orderString = "ORDER BY "
                for prop in orderBy["properties"]:
                    orderString += "{}.{} ".format(prop["element"], prop["property"])

                orderString += orderBy["direction"].upper()

            cypherQuery = "MATCH (n:"+nodeALabelsString+" {actorId: {nodeAProperties}.actorId})-[r:"+relationshipLabelsString+"]->(n2:"+nodeBLabelsString+") RETURN n2,r "+orderString+" LIMIT "+str(limit)
            results = session.run(statement=cypherQuery, nodeAProperties=nodeAProperties)

            resultList = []
            for record in results.records():
                resultDict = {
                    "node":{},
                    "relationship":{}
                }

                for key in record["n2"].keys():
                    resultDict["node"][key] = record["n2"][key]

                for key in record["r"].keys():
                    resultDict["relationship"][key] = record["r"][key]

                resultList.append(resultDict)

            return resultList
