from tkinter import *

from MapElement import MapElement

class Grass(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='../Images/grass.png')

    def action(self):
        pass
    
    def isPassable(self):
        return False
