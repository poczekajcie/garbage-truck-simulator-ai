from tkinter import *
from MapElement import MapElement

class Dump(MapElement):
    def __init__(self, x, y, type):
        self.position = [x,y]
        self.type = type 
        if type == 'paper':
            self.image = PhotoImage(file='../Images/paper.png')
        elif type == 'plastic':
            self.image = PhotoImage(file='../Images/plastic.png')
        elif type == 'glass':
            self.image = PhotoImage(file='../Images/glass.png')
        else:
            self.image = PhotoImage(file='../Images/other.png')

    def action(self):
        pass
    
    def isPassable(self):
        return False
