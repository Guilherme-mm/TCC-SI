from enum import Enum, unique
from .Operation import Operation
from .SetLogPathOperation import SetLogPathOperation

@unique
class OperationCode(Enum):
    SET_LOG_PATH = 1
    UPDATE_MODEL = 2
    SET_SIMILARITY_ENGINE = 3

    def instantiateOperation(self) -> Operation:
        instanceValue = self.value
        if instanceValue == 1: # pylint: disable=comparison-with-callable
            return SetLogPathOperation()
