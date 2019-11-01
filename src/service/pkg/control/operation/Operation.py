from abc import ABC, abstractmethod
from ...model.message.NetworkMessage import NetworkMessage

class Operation(ABC):
    @abstractmethod
    def execute(self) -> NetworkMessage:
        pass
