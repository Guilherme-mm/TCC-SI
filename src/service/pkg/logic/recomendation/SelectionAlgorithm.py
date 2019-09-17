from abc import ABC, abstractmethod

class SelectionAlgorithm(ABC):

    @abstractmethod
    def getRecommendations(self):
        pass
