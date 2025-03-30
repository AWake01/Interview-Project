#controller.py
import model
from view import BoardView
from model import BoardModel

echoPatten = "(?P<opp>E) (?P<seq>[0-9a-f]{2})$"
inputPattern = "(?P<opp>I) (?P<seq>[0-9a-f]{2}) (?P<typ>[AD])(?P<dir>[IO])(?P<pin>[0-9a-f]{2})$"
powerPattern = "(?P<opp>P) (?P<seq>[0-9a-f]{2}) (?P<pow>[01])$"
outputDigitalPattern = "(?P<opp>O) (?P<seq>[0-9a-f]{2}) (?P<typ>DO)(?P<pin>[0-9a-f]{2}) (?P<out>[01])$"
outputAnaloguePattern = "(?P<opp>O) (?P<seq>[0-9a-f]{2}) (?P<typ>AO)(?P<pin>[0-9a-f]{2}) (?P<out>[0-9a-f]{8})$"

#Bridge between model (control board) and view (terminal input)
class BoardController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    #Convert user input to command format
    def __convert_input_to_command(self, input):
        command = f"^{input}\n"
        return command

    #Convert model response to readable format
    def __convert_response_to_reply(self, response):
        response = response[1:]  # Strip prepending ^
        response = response.rstrip()  # Remove trailing \n
        reply = f"{response}"
        return reply

    #Pass input from view to model. Pass response from model to view
    def receive_input(self, input):
        if input == "D":            #DEBUG: View current sensor states
            self._model.debug_print()
            return "DEBUG"
        command = self.__convert_input_to_command(input)
        response = self._model.receive_command(command)
        reply = self.__convert_response_to_reply(response)
        return reply


model = BoardModel()
view  = BoardView()
controller = BoardController(model, view)
