from tkinter import *

from MapElement import MapElement


class Bin(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='../Images/house.png')
        self.state = 'full'
        self.visited = False

    def action(self):
        pass

    def empty(self):
        self.image = PhotoImage(file='../Images/houseUpdate.png')
        self.state = 'empty'

    def isPassable(self):
        return False
