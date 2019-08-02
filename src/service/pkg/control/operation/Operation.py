from abc import ABC, abstractmethod
from ...api.ApiMessage import ApiMessage

class Operation(ABC):
    @abstractmethod
    def execute(self) -> ApiMessage:
        pass
