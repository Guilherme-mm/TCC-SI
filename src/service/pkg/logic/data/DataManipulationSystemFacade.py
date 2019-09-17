from typing import Generator
from .ClientDataManager import ClientDataManager
from ...database.storage.ConfigurationsManager import ConfigurationsManager
from ...model.log.LogEntry import LogEntry

class DataManipulationSystemFacade():
    def __init__(self):
        print("Data manipulation subsystem facade instantiated")

    def collectClientLogData(self) -> Generator:
        print("Starting log data extraction...")
        configManager = ConfigurationsManager()
        clientLogPath = configManager.getConfiguration("clientLogPath")
        print("The configured log path is [{}]".format(clientLogPath))

        totalLineNumber = 0
        with open(clientLogPath, 'r') as dataFile:
            print("Determining file size...")

            for line in dataFile:
                totalLineNumber += 1

            print("Lines to read: {}".format(totalLineNumber))

        with open(clientLogPath, 'r') as dataFile:
            currentLine = 0
            lastPercentage = None
            for line in dataFile:
                currentPercentage = int((currentLine * 100)/totalLineNumber)
                if currentPercentage != lastPercentage:
                    print("Progress: {}%".format(currentPercentage))
                    lastPercentage = currentPercentage

                currentLine += 1
                linePositions = line.split('\t')
                logEntry =  LogEntry(linePositions[0], "rated", linePositions[1], linePositions[2])
                yield logEntry

    def persistClientData(self, clientData, dataMap):
        clientDataManager = ClientDataManager()
        return clientDataManager.persistClientData(clientData, dataMap)
