#model.py
import random
import re       #Regex patten matching for command decoding
import pandas   #For printing debug table

#Regex patterns for command decoding
echoPatten = "(?P<opp>E) (?P<seq>[0-9a-f]{2})$"
inputPattern = "(?P<opp>I) (?P<seq>[0-9a-f]{2}) (?P<typ>[AD])(?P<dir>[IO])(?P<pin>[0-9a-f]{2})$"
powerPattern = "(?P<opp>P) (?P<seq>[0-9a-f]{2}) (?P<out>[01])$"
outputAnaloguePattern = "(?P<opp>O) (?P<seq>[0-9a-f]{2}) (?P<typ>A)(?P<dir>O)(?P<pin>[0-9a-f]{2}) (?P<out>[0-9a-f]{8})$"
outputDigitalPattern = "(?P<opp>O) (?P<seq>[0-9a-f]{2}) (?P<typ>D)(?P<dir>O)(?P<pin>[0-9a-f]{2}) (?P<out>[01])$"


#Input and output devices are modedld together as a single 'Sensor' object
class Sensor:
    def __init__(self, port, type, state, power):
        self._port = port    #Channel number
        self._type = type    # Analogue A, Digital D
        self._state = state  #Fixed at initialisation
        self._power = power  #OFF 0, ON 20

    def get_state(self):
        return self._state
    def get_type(self):
        return self._power
    def get_power(self):
        return self._state

    #Set sensor state (UNUSED)
    def set_state(self, _state):
        self.state = _state

class BoardModel:
    def __init__(self):
        #self.controller = BoardController()
        self._powerUp = 0                                                    #Set to off

        self._sensors = []
        self._sensors.append(Sensor(0, "D", 1, 0))      #Digital input 1  - light
        self._sensors.append(Sensor(1, "D", 0, 0))      #Digital input 2  - motion
        self._sensors.append(Sensor(2, "A", 225, 0))    #Analouge input 1 - detected power W
        self._sensors.append(Sensor(3, "A", 0, 0))      #Analouge input 2 - distance mm

        #DEBUG: Store last commands sent and received
        self._debuglastComandReceived = ""
        self._debuglastResponseSent = ""

    #Get all sensor objects
    def get_sensors(self):
        return self._sensors

    #Get current power state
    def get_power(self):
        return self._powerUp

    #Set current board power state.
    def set_power(self, _value):
        self._powerUp = _value
        self.__power_sensors(_value) #Set power on all sensors

    #Set power on all sensors
    def __power_sensors(self, value):
        _setPower = 0
        if value == "1":
            _setPower = 20
        elif value == "0":
            _setPower = 0

        for sensor in self._sensors:
            sensor.power = _setPower

    def generate_mock_analouge(self):
        return random.randrange(0,4294967295)     #00000000 to ffffffff

    def generate_mock_digital(self):
        return random.randint(0,1)     #0 or 1

    #Process received command from controller and construct reply
    def __process_command(self, command):
        #Match commands to Regex patterns
        match = re.match(echoPatten, command) or re.match(powerPattern, command) or re.match(inputPattern, command) or re.match(outputDigitalPattern, command) or re.match(outputAnaloguePattern, command)
        try: operation = match.group("opp")
        except: operation = None
        try: sequence = match.group("seq")
        except: sequence = None
        try: type = match.group("typ")
        except: type = None
        try:direction = match.group("dir")
        except: direction = None
        try: port = match.group("pin")
        except: port = None
        try: output = match.group("out")
        except: output = None

        response = ""
        if not match: response = "ERR"  #ERR: displayed when command is incorrectly formatted
        else:
            #ECHO command
            if operation == "E":
                returnCode = "OK_"
                reply = self.__echo_cmd()
                response = f"{operation} {sequence} {returnCode} {reply}"
            #POWER UP STATE command
            elif operation == "P":
                self.__power_cmd(output)
                response = f"{operation} {sequence} OK_\n"
            #OUTPUT command
            #elif match.group("opp") == "O" and match.group("typ") in ["D", "A"]:
            elif operation == "O":
                port = int(port, 16)   #Hex to dec
                boardResponse = self.__out_command(type, direction, port, output)
                response = f"{operation} {sequence} {boardResponse}"
            #INPUT command
            else:
                port = int(port, 16)  # Hex to dec
                boardResponse = self.__in_command(type, direction, port)
                try: response = f"{operation} {sequence} {boardResponse[0]} {boardResponse[1]}" #hex(boardReading[1]
                except: response = f"{operation} {sequence} {boardResponse[0]}"

        return self.__create_command(response)

    def receive_command(self, command):
        #self.window.displayLbl.text = command
        self.debuglastComandReceived = command    #DEBUG: save last received command
        newCommand = self.__strip_command(command)
        response = self.__process_command(newCommand)
        self.debuglastResponseSent = response  # DEBUG: save last sent response
        return response

    def __strip_command(self, command):
        command = command[1:]    #Strip prepending ^
        command = command.rstrip()         #Remove trailing \n
        return command

    def __create_command(self, command):
        command = f"^{command}\n"
        return command

    # Check if sensor type and port matches an existing device
    def check_port(self, type, dir, port):
        portValid = [s for s in self._sensors if s._type == type and s._port == port]  #Find sensor with matching type and port
        if portValid:
            return portValid[0]                                                     #Return matching sensor object
        else:
            return False

    # Impliments 'Output' command for digital outputs to set power to input devices
    def __out_command(self, type, dir, port, out):
        portValid = self.check_port(type[0], dir, port)  # A D type
        #self.sensor.state = out
        if portValid:
            sensor = portValid
            if out == "1":                               #Switch power on
                sensor._power = 20
            elif out == "0":                             #Switch power off
                sensor._power = 0
            return "OK_"
        else:
            return "RNG_"                                #Incorrect channel selected

    #Impliments 'Input' command for analogue and digital inputs, reading both input and output direction
    def __in_command(self, type, dir, port):
        portValid = self.check_port(type, dir, port)  # A D type
        #self.sensor.state = out
        if portValid:
            sensor = portValid
            reply = ""
            if dir == "I" and sensor._power == 20:   #Input is powered
                reply = sensor._state
            elif dir == "O":                        #Report power state
                reply = sensor._power
            #self.__out_command(portExists, )
            return ["OK_", reply]
        else:
            return ["RNG_"]


    #Impliment 'Echo' command to get the current power state of the board
    def __echo_cmd(self):
        power = self.get_power()
        if int(power) == 1:
            return "PWR"
        elif int(power) == 0:
            return "OFF"

    #Impliment '4.4	Power Up State' command to set the current power state of the board
    def __power_cmd(self, state):
        powerUp = self.set_power(state) #Sets board power and power to all sensors

    #DEBUG: Print out current sensor values. Called directly from console, instead of passed to model as command. Prints directly to console, not view
    #       Also print last received/sent messages to model
    def debug_print(self):
        df = pandas.DataFrame.from_records([s.__dict__ for s in self._sensors])
        print(df)
        print(f"Last command: {self._debuglastComandReceived}")
        print(f"Last response: {self._debuglastResponseSent}")