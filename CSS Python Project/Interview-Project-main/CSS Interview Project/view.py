#view.py

#View uses python command line console input
class BoardView:
    def __init__(self):
        self.controller = None

    #Loop to prompt for input from user and write output to console. X can be used to exit the program.
    def read_input_start(self):
        print("\nSTART - Enter E, I, O or P commands, or X to exit...")
        while True:
            #print(input)
            userInput = input("$: ")
            if userInput == "X":            #End program
                print("CLOSE")
                exit()
            output = self.controller.receive_input(userInput)
            self.__write_output(output)

    #Display controller reply to user
    def __write_output(self, output):
        print(f"{output}")

#ontroller = BoardController(BoardModel)
view = BoardView()
