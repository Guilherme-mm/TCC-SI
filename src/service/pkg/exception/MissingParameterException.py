class MissingParameterException(Exception):
    """
        Raised when a expected parameter is not provided
    """
    def __init__(self, errorMessage:str = ""):
        super(MissingParameterException, self).__init__()
        self.message = "A required parameter was not provided"
        self.errorMessage = errorMessage
