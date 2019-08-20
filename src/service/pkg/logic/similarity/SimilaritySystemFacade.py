from .SimilarityAlgorithmsTypes import SimilarityAlgorithmsTypes
from ..data.DataManipulationSystemFacade import DataManipulationSystemFacade
from ...database.managers.ConfigurationsManager import ConfigurationsManager

class SimilaritySystemFacade():
    def __init__(self):
        pass

    def calculateSimilarities(self):
        # Map of actors and actions over objects
        actorsDict = {}

        # Getting the current settings of the application
        configManager = ConfigurationsManager()
        dataSystemFacade = DataManipulationSystemFacade()
        configuredSimilarityEngineName = configManager.getConfiguration("similarityEngine")
        simAlgorithmsTypes = SimilarityAlgorithmsTypes(configuredSimilarityEngineName)
        configuredSimilarityEngine = simAlgorithmsTypes.instantiateSimilarityAlgorithm()

        # Iterating over the lines of the data file and populating the actorsDict
        logEntriesGenerator = dataSystemFacade.collectClientLogData()
        for entry in logEntriesGenerator:
            actor = entry.getActor()
            action = entry.getAction()
            print("processing {} on {}".format(actor, action))

            if actorsDict.get(actor, None) is None:
                actorsDict[actor] = {}
                if actorsDict.get(actor).get(action, None) is None:
                    actorsDict[actor][action] = []

            actorsDict[actor][action].append(entry.getActionObject())

        # Sends the dict to the similarity engine to generate the distances matrix
        distancesMatrix = configuredSimilarityEngine.calculateSimilarities(actorsDict)

    def generateClusters(self):
        pass

    def getRecommendation(self):
        pass
