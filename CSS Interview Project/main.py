#main.py
import subprocess

from controller import BoardController
from model import BoardModel
from view import BoardView
from controller import BoardController

# Create instances of model, view and controller
model = BoardModel()
view = BoardView()
controller = BoardController(model, view)
view.controller = controller

#Run instances of model.py and view.py
subprocess.run(["python", "model.py"])
subprocess.run(["python", "view.py"])

while(True):
    #userInput = input("$: ")
    view.read_input_start()