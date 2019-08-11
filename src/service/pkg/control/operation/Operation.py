from abc import ABC, abstractmethod
from ...model.message.ApiMessage import ApiMessage

class Operation(ABC):
    @abstractmethod
    def execute(self) -> ApiMessage:
        pass
