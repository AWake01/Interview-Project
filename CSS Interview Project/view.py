#view.py

#View uses python command line console input
class BoardView:
    def __init__(self):
        self._controller = None

    #Loop to prompt for input from user and write output to console
    def read_input_start(self):
        while True:
            #print(input)
            userInput = input("$: ")
            self.__write_output(self._controller.receive_input(userInput))

    #Display controller reply to user
    def __write_output(self, output):
        print(f"{output}")

#ontroller = BoardController(BoardModel)
view = BoardView()
