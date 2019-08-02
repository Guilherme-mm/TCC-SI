from enum import Enum, unique
from .Operation import Operation
from .SetLogPathOperation import SetLogPathOperation

@unique
class OperationCode(Enum):
    SET_LOG_PATH = 1

    def instantiateOperation(self) -> Operation:
        instanceValue = self.value
        if instanceValue == 1:
            return SetLogPathOperation()
