from .SelectionAlgorithmsTypes import SelectionAlgorithmsTypes
from ...database.storage.ConfigurationsManager import ConfigurationsManager

class RecommendationsManager():
    def __init__(self):
        self.__configManager = ConfigurationsManager()
        configuredSelectionAlgorithm = self.__configManager.getConfiguration("selectionAlgorithm")
        selectionTypes = SelectionAlgorithmsTypes(configuredSelectionAlgorithm)
        self.__selectionAlgorithm = selectionTypes.instantiateSelectionAlgorithm()

    def getRecommendations(self, actorId, quantity):
        recommendations = self.__selectionAlgorithm.getRecommendations(actorId, quantity)
        return recommendations
