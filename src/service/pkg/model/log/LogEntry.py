class LogEntry():
    def __init__(self, actor:str = "", action:str = "", actionObject:str = ""):
        self.__actor = actor
        self.__action = action
        self.__actionObject = actionObject

    def setActor(self, actor:str) -> bool:
        self.__actor = actor

    def setAction(self, action:str) -> bool:
        self.__action = action

    def setActionObject(self, actionObject:str) -> bool:
        self.__actionObject = actionObject

    def getActor(self) -> str:
        return self.__actor

    def getAction(self) -> str:
        return self.__action

    def getActionObject(self) -> str:
        return self.__actionObject
