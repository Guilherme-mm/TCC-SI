from .RecommendationsManager import RecommendationsManager

class RecommendationSystemFacade():
    def __init__(self):
        pass

    def getRecommendations(self, actorId, quantity, K:int=5):
        recommendationsManager = RecommendationsManager()
        return recommendationsManager.getRecommendations(actorId, quantity, K)

    def testRecommendationsAccuracy(self, quantity:int, K:int):
        recommendationsManager = RecommendationsManager()
        return recommendationsManager.testRecommendationsAccuracy(quantity, K)
