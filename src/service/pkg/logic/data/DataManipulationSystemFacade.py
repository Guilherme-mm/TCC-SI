from typing import Generator
from .ClientDataManager import ClientDataManager
from ...database.storage.ConfigurationsStorage import ConfigurationsStorage
from ...model.log.LogEntry import LogEntry
from ...utils.ClientCommunicationUtils import ClientCommunicationUtils

class DataManipulationSystemFacade():
    def __init__(self):
        print("Data manipulation subsystem facade instantiated")

    def collectClientLogData(self) -> Generator:
        configManager = ConfigurationsStorage()
        clientLogPath = configManager.getConfiguration("clientLogPath")
        fileHasHeader = configManager.getConfiguration("dataFileHasHeader")
        dataSeparator = configManager.getConfiguration("dataFileSeparator")

        ClientCommunicationUtils.sendMessage("Extracting log data from {}".format(clientLogPath))

        skippedFirstLine = False
        with open(clientLogPath, 'r') as dataFile:
            for line in dataFile:
                if fileHasHeader and (not skippedFirstLine):
                    skippedFirstLine = True
                    continue

                linePositions = line.split(dataSeparator)
                logEntry = LogEntry(linePositions[0], "rated", linePositions[1], linePositions[2])
                yield logEntry

    def getClientDataRowsCnt(self) -> int:
        configManager = ConfigurationsStorage()
        clientDataFilePath = configManager.getConfiguration("clientLogPath")
        fileHasHeader = configManager.getConfiguration("dataFileHasHeader")

        totalLineNumber = 0
        skippedFirstLine = False
        with open(clientDataFilePath, 'r') as dataFile:
            for line in dataFile:
                if fileHasHeader and (not skippedFirstLine):
                    skippedFirstLine = True
                    continue

                totalLineNumber += 1

        return totalLineNumber

    def persistClientData(self, clientData, dataMap):
        clientDataManager = ClientDataManager()
        return clientDataManager.persistClientData(clientData, dataMap)

    def collectTestData(self) -> Generator:
        configManager = ConfigurationsStorage()
        testDataFilePath = configManager.getConfiguration("testDataPath")

        with open(testDataFilePath, 'r') as dataFile:
            for line in dataFile:
                linePositions = line.split('\t')
                logEntry =  LogEntry(linePositions[0], "rated", linePositions[1], linePositions[2])
                yield logEntry

    def getTestDataRowsCnt(self) -> int:
        configManager = ConfigurationsStorage()
        testDataFilePath = configManager.getConfiguration("testDataPath")

        totalLineNumber = 0
        with open(testDataFilePath, 'r') as dataFile:
            for line in dataFile:
                totalLineNumber += 1

        return totalLineNumber

    def clearClientData(self):
        clientDataManager = ClientDataManager()
        return clientDataManager.wipeClientData()
        