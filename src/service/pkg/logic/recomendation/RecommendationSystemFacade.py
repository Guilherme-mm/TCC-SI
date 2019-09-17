from .RecommendationsManager import RecommendationsManager

class RecommendationSystemFacade():
    def __init__(self):
        pass

    def getRecommendations(self, actorId, quantity):
        recommendationsManager = RecommendationsManager()
        return recommendationsManager.getRecommendations(actorId, quantity)
