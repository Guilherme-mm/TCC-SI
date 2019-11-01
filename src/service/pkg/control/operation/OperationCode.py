from enum import Enum, unique
from .Operation import Operation
from .SetLogPathOperation import SetLogPathOperation

@unique
class OperationCode(Enum):
    SET_LOG_PATH = 1
    UPDATE_MODEL = 2
    SET_SIMILARITY_ENGINE = 3
    SET_CLUSTER_ALGORITHM = 4
    SET_RECOMMENDATION_SELECTION_ALGORITHM = 5
    GET_RECOMMENDATIONS = 6
    SET_TEST_DATA_PATH = 7
    TEST_RECOMMENDATIONS_ACCURACY = 8
    CLEAR_GRAPH_DB = 9
    CLEAR_DATA_DB = 10
    GET_CONFIGURATION_VALUE = 11

    def instantiateOperation(self) -> Operation:
        instanceValue = self.value
        if instanceValue == 1: # pylint: disable=comparison-with-callable
            return SetLogPathOperation()
