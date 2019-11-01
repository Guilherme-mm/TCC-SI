from .SelectionAlgorithmsTypes import SelectionAlgorithmsTypes
from ...database.storage.ConfigurationsStorage import ConfigurationsStorage
from ..data.DataManipulationSystemFacade import DataManipulationSystemFacade

class RecommendationsManager():
    def __init__(self):
        self.__configManager = ConfigurationsStorage()
        configuredSelectionAlgorithm = self.__configManager.getConfiguration("selectionAlgorithm")
        selectionTypes = SelectionAlgorithmsTypes(configuredSelectionAlgorithm)
        self.__selectionAlgorithm = selectionTypes.instantiateSelectionAlgorithm()

    def getRecommendations(self, actorId, quantity):
        recommendations = self.__selectionAlgorithm.getRecommendations(actorId, quantity)
        return recommendations

    def testRecommendationsAccuracy(self):
        print("Opening a generator for the test data file")
        dataSystemFacade = DataManipulationSystemFacade()

        testLogEntriesGenerator =  dataSystemFacade.collectTestData()

        actorsDict = {}
        print("Interating over test data and getting recommendations")
        for entry in testLogEntriesGenerator:
            if not actorsDict.get(entry.getActor(), False):
                actorsDict[entry.getActor()] = {}

            if not actorsDict[entry.getActor()].get(entry.getActionObject(), False):
                actorsDict[entry.getActor()][entry.getActionObject()] = {}

            actorsDict[entry.getActor()][entry.getActionObject()]["realValue"] = int(entry.getValue())

            recommendations = self.getRecommendations(entry.getActor(), 30)

            for recommendation in recommendations:
                if recommendation["objectId"] == entry.getActionObject():
                    actorsDict[entry.getActor()][entry.getActionObject()]["recommendedValue"] = recommendation["value"]
                    break

        variancesList = []
        totalItems = 0
        totalItemsWithoutRecommendation = 0

        for actor in actorsDict.values():
            for actionObject in actor.values():

                totalItems = totalItems + 1
                if not actionObject.get("recommendedValue", False):
                    totalItemsWithoutRecommendation = totalItemsWithoutRecommendation + 1
                    continue

                actionObject["realValue"] = actionObject["realValue"]
                actionObject["recommendedValue"] = int(actionObject["recommendedValue"])
                # print("Real: {}, Reco: {}".format(actionObject["realValue"], actionObject["recommendedValue"]))
                variation = ((actionObject["realValue"] - actionObject["recommendedValue"])/actionObject["realValue"]) * 100
                print("real: {}, reco: {}, variance: {}".format(actionObject["realValue"], actionObject["recommendedValue"], variation))
                variancesList.append(abs(variation))

        return {
            "variationAvg": sum(variancesList)/len(variancesList),
            "missedRecommendations": totalItemsWithoutRecommendation
        }
        # return 
