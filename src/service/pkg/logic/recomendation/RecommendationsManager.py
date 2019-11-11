from .SelectionAlgorithmsTypes import SelectionAlgorithmsTypes
from ..data.DataManipulationSystemFacade import DataManipulationSystemFacade
from ...database.storage.ConfigurationsStorage import ConfigurationsStorage
from ...utils.ClientCommunicationUtils import ClientCommunicationUtils

class RecommendationsManager():
    def __init__(self):
        self.__configManager = ConfigurationsStorage()
        configuredSelectionAlgorithm = self.__configManager.getConfiguration("selectionAlgorithm")
        selectionTypes = SelectionAlgorithmsTypes(configuredSelectionAlgorithm)
        self.__selectionAlgorithm = selectionTypes.instantiateSelectionAlgorithm()

    def getRecommendations(self, actorId, quantity, K):
        recommendations = self.__selectionAlgorithm.getRecommendations(actorId, quantity, K)
        return recommendations

    def testRecommendationsAccuracy(self, recommendationsQuantity:int=10, K:int=5):
        ClientCommunicationUtils.sendMessage("Starting test data collection...")

        dataSystemFacade = DataManipulationSystemFacade()
        testLogEntriesGenerator =  dataSystemFacade.collectTestData()
        totalLogEntries = dataSystemFacade.getTestDataRowsCnt()
        actorsDict = {}
        entriesCounter = 0

        ClientCommunicationUtils.sendMessage("Done!")
        ClientCommunicationUtils.sendMessage("Processing test data...")

        # For each log entry on the test dataset...
        for entry in testLogEntriesGenerator:
            entriesCounter = entriesCounter +1

            # Adds the actor on the dict if it desnt exists
            if not actorsDict.get(entry.getActor(), False):
                actorsDict[entry.getActor()] = {}

            # Adds the object to the actor if it doesnt exists
            if not actorsDict[entry.getActor()].get(entry.getActionObject(), False):
                actorsDict[entry.getActor()][entry.getActionObject()] = {}

            # Saves on the object the real value finded in the test data
            actorsDict[entry.getActor()][entry.getActionObject()]["realValue"] = float(entry.getValue())
            # Requests N recommendations to the current entry actor
            recommendations = self.getRecommendations(entry.getActor(), recommendationsQuantity, K)

            # Checks if the current log entry object is present on the recommendations...
            for recommendation in recommendations:
                # if it is, adds to the object in the dict value and weighted value presented in the recommendation
                if recommendation["objectId"] == entry.getActionObject():
                    actorsDict[entry.getActor()][entry.getActionObject()]["recommendedValue"] = recommendation["value"]
                    actorsDict[entry.getActor()][entry.getActionObject()]["weightedRecommendedValue"] = recommendation["weightedValue"]
                    break

            ClientCommunicationUtils.sendProgress((entriesCounter * 100)/totalLogEntries)

        ClientCommunicationUtils.sendMessage("Calculating MAE, MWE and counting Recall...")

        variancesList = []
        weightedVariancesList = []
        totalItems = 0
        totalItemsWithoutRecommendation = 0
        actorsCounter = 0
        totalActors = len(actorsDict.values())

        # print(actorsDict)

        for actor in actorsDict.values():
            actorsCounter = actorsCounter + 1

            for actionObject in actor.values():
                totalItems = totalItems + 1

                if not actionObject.get("recommendedValue", False):
                    totalItemsWithoutRecommendation = totalItemsWithoutRecommendation + 1
                    continue

                # actionObject["realValue"] = actionObject["realValue"]
                actionObject["recommendedValue"] = float(actionObject["recommendedValue"])

                variation = ((actionObject["realValue"] - actionObject["recommendedValue"])/actionObject["realValue"]) * 100
                weightedVariation = ((actionObject["realValue"] - actionObject["weightedRecommendedValue"])/actionObject["realValue"]) * 100

                variancesList.append(abs(variation))
                weightedVariancesList.append(abs(weightedVariation))
                print("R: {}, RC: {}, WRC: {}, V: {}, WV: {}".format(actionObject["realValue"], actionObject["recommendedValue"], actionObject["weightedRecommendedValue"], variation, weightedVariation))

            ClientCommunicationUtils.sendProgress((actorsCounter * 100)/totalActors)

        # print(variancesList)

        return {
            "variationAvg": sum(variancesList)/len(variancesList),
            "weightedVariationAvg": sum(weightedVariancesList)/len(weightedVariancesList),
            "missedRecommendations": totalItemsWithoutRecommendation
        }
