from abc import ABC, abstractmethod

class NetworkCommunicationManager(ABC):
    @abstractmethod
    def up(self):
        pass

    @abstractmethod
    def registerObserver(self, observer):
        pass

    @abstractmethod
    def unregisterObserver(self, observer):
        pass