from tkinter import *

from MapElement import MapElement

class Road(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='road.png')

    def action(self):
        pass

    def display(self):
