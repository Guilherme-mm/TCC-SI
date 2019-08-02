from abc import ABC, abstractmethod

class NetworkComunicationManager(ABC):
    @abstractmethod
    def up(self):
        pass

    @abstractmethod
    def registerObserver(self, observer):
        pass

    @abstractmethod
    def unregisterObserver(self, observer):
        pass