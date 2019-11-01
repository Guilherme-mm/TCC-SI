from abc import ABC, abstractmethod

from ..model.message.NetworkMessage import NetworkMessage

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

    @abstractmethod
    def sendMessage(self, message:NetworkMessage):
        pass
