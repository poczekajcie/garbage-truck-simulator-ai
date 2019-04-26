
from tkinter import *
from MapElement import MapElement


class Road(MapElement):
    def __init__(self, x, y):
        self.position = [x, y]
        self.image = PhotoImage(file='Images/road.png')

    def action(self):
        pass

    def isPassable(self):
        return True
