from typing import Generator
from ...database.managers.ConfigurationsManager import ConfigurationsManager
from ...model.log.LogEntry import LogEntry

class DataManipulationSystemFacade():
    def __init__(self):
        pass

    def collectClientLogData(self) -> Generator:
        configManager = ConfigurationsManager()
        clientLogPath = configManager.getConfiguration("clientLogPath")

        with open(clientLogPath, 'r') as dataFile:
            for line in dataFile:
                linePositions = line.split('\t')
                print(linePositions)
                logEntry =  LogEntry(linePositions[0], "rated", linePositions[1])
                yield logEntry
