from .Operation import Operation
from ...model.message.ApiMessage import ApiMessage

class SetLogPathOperation(Operation):

    def execute(self) -> ApiMessage:
        yield "Consegui"
        yield "a parada"
        yield "funciona!"
