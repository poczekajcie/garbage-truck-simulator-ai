from tkinter import *
from random import randint
from Collector import Collector
from MapElement import MapElement
from Road import Road
from Grass import Grass
from Dump import Dump
from Bin import Bin
from State import State
import time
import sys
sys.setrecursionlimit(3000)

class Simulation(object):

##################################################################### PODSTAWOWE METODY
    def checkIfPositionIsEmpty(self, position):
        for i in self.mapElements:
            if i.position == position:
                return False
        return True

    def returnElementAhead(self):
        pass

##################################################################### GENEROWANIE MAPY
    def __init__(self, binsAmount):
        self.gridWidth = 20
        self.gridHeight = 9
        self.fieldSize = 64
        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.fieldSize*self.gridWidth, height = self.fieldSize*self.gridHeight)
        self.binsAmount = binsAmount
        self.window.title("Simulation")
        self.collector = Collector(1, 1, 2)
        self.mapElements = []
        self.grid = []
        self.makeGrid()
        self.grassImage = PhotoImage(file='Images/grass.png')
        self.addDumps()
        self.addRoads()
        self.addBins()
        self.addGrass()
        self.collector.position = [1,1]
        self.results = []
        self.dfs(self.grid, [], self.collector.position)
        self.getBestWay(self.results)


    def makeGrid(self):
        for i in range(self.gridHeight):
            self.grid.append([0] * self.gridWidth)
    
    
    def addDumps(self):
        types = ['plastic', 'paper', 'glass', 'other']
        n = 0
        for j in types:
            new = Dump(n, 0, j)
            self.grid[0][n] = new
            n = n + 1 
            self.mapElements.append(new)

    
    def addRoad(self, position1, position2):
        if position1[0]==position2[0]:
            for i in range(position1[1], position2[1]+1):
                if self.checkIfPositionIsEmpty([position1[0], i]):
                    element = Road(position1[0], i)
                    self.mapElements.append(element)
                    self.grid[i][position1[0]] = element
        elif position1[1]==position2[1]:
            for i in range(position1[0], position2[0]):
                if self.checkIfPositionIsEmpty([i, position1[1]]):
                    element = Road(i, position1[1])
                    self.mapElements.append(element)
                    self.grid[position1[1]][i] = element

    def addRoads(self):
        self.addRoad([0,1],[self.gridWidth,1])
        self.addRoad([0,4],[self.gridWidth,4])
        self.addRoad([0,7],[self.gridWidth,7])
        r = randint(1, 6)
        for i in range(0, r):
            s = randint(1, self.gridWidth-2)
            self.addRoad([s, 1],[s, self.gridHeight-2])

    def addBins(self):
        for i in range(0, self.binsAmount):
            rightPosition = False
            while not rightPosition:
                x = randint(0, self.gridWidth - 1)
                y = randint (0, self.gridHeight - 1)
                if self.checkIfPositionIsEmpty([x,y]):
                    rightPosition = True
            element = Bin(x, y)
            self.mapElements.append(element)
            self.grid[y][x] = element

    def addGrass(self):
        for i in range (0, self.gridWidth):
            for j in range (0, self.gridHeight):
                if self.checkIfPositionIsEmpty([i,j]):
                    element = Grass(i,j)
                    self.mapElements.append(element)
                    self.grid[j][i] = element

    def display(self):
        for i in self.mapElements:
            x = i.position[0]
            y = i.position[1]
            self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=i.image, anchor=NW)
        x = self.collector.state.position[0]
        y = self.collector.state.position[1]
        self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=self.collector.image, anchor=NW)
        self.canvas.pack()

    def update(self):
        self.display()
        self.window.update_idletasks()
        self.window.update()
        time.sleep(1.5)
    
    def start(self):
        while True:
            self.moveCollector()

##################################################################### RUCH AGENTA 
    def moveCollector(self):
        self.update()
        self.collector.turnLeft()

    def DoPossibleMove(self, direction):
        return direction

##################################################################### DFS

    def dfs(self, grid, listOfSteps, collectorPosition):
        if self.isTheEnd(grid):
            self.results.append(listOfSteps)
        else:
            for possibility in self.findPossibilities(grid, collectorPosition):
                collectorPosition = self.DoPossibleMove(possibility)
                grid = self.emptyHouseIfIsFull(grid, collectorPosition)
                listOfSteps.append(possibility)
                return self.dfs(grid, listOfSteps, collectorPosition)

    def isTheEnd(self, grid):
        for i in range(0, self.gridHeight):
            for object in grid[i]:
                if isinstance(object, Bin):
                    if object.state == 'full':
                        return False
        return True

    def findPossibilities(self, grid, collectorPosition):
        possibleMoves = []
        #left
        if (collectorPosition[0]-1 >= 0) and (isinstance(grid[collectorPosition[1]][collectorPosition[0]-1], Road)):
            possibleMoves.append([collectorPosition[0]-1, collectorPosition[1]])
        #right
        if (collectorPosition[0] + 1 < self.gridWidth) and (isinstance(grid[collectorPosition[1]][collectorPosition[0] + 1], Road)):
            possibleMoves.append([collectorPosition[0] + 1, collectorPosition[1]])
        #up
        if (collectorPosition[1] - 1 >= 0) and (isinstance(grid[collectorPosition[1] - 1][collectorPosition[0]], Road)):
            possibleMoves.append([collectorPosition[0], collectorPosition[1] - 1])
        #down
        if (collectorPosition[1] + 1 < self.gridHeight) and (isinstance(grid[collectorPosition[1] + 1][collectorPosition[0]], Road)):
            possibleMoves.append([collectorPosition[0], collectorPosition[1] + 1])
        return possibleMoves

    def emptyHouseIfIsFull(self, grid, collectorPosition):

        # left
        if (collectorPosition[0] - 1 >= 0) and (isinstance(grid[collectorPosition[1]][collectorPosition[0] - 1], Bin)):
            if grid[collectorPosition[1]][collectorPosition[0] - 1].state == 'full':
                grid[collectorPosition[1]][collectorPosition[0] - 1].state = 'empty'

        # right
        if (collectorPosition[0] + 1 < self.gridWidth) and (isinstance(grid[collectorPosition[1]][collectorPosition[0] + 1], Bin)):
            if grid[collectorPosition[1]][collectorPosition[0] + 1].state == 'full':
                grid[collectorPosition[1]][collectorPosition[0] + 1].state = 'empty'

        # up
        if (collectorPosition[1] - 1 >= 0) and (isinstance(grid[collectorPosition[1] - 1][collectorPosition[0]], Bin)):
            if grid[collectorPosition[1] - 1][collectorPosition[0]].state == 'full':
                grid[collectorPosition[1] - 1][collectorPosition[0]].state = 'empty'

        # down
        if (collectorPosition[1] + 1 < self.gridHeight) and (isinstance(grid[collectorPosition[1] + 1][collectorPosition[0]], Bin)):
            if grid[collectorPosition[1] + 1][collectorPosition[0]].state == 'full':
                grid[collectorPosition[1] + 1][collectorPosition[0]].state = 'empty'

        return grid


    def getBestWay(self, results):
        print("no beda xd")

