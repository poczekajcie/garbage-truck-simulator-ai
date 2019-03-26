from tkinter import *

from MapElement import MapElement

class Bin(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='Images/house.png')
        self.state = 'full'

    def action(self):
        pass

    def isPassable(self):
        return False
