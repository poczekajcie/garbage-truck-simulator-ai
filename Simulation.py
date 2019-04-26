import collections
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
        self.results = []
        self.bfs_wrapper(self.grid, self.collector.state.position)


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
        time.sleep(0.2)
    
    def start(self):
        while True:
            self.moveCollector()

##################################################################### RUCH AGENTA 
    def moveCollector(self):
        self.update()
        while self.results:
            path = self.results.pop(0)
            step = path.pop(0)
            while True:
                # print(self.collector.state.position, step, path)
                if self.collector.state.position == step:
                    if path:
                        step = path.pop(0)
                else:
                    if self.collector.state.rotation == self.cords_to_rotation(self.collector.state.position, step):
                        self.collector.goAhead()
                    elif (self.collector.state.rotation - self.cords_to_rotation(self.collector.state.position, step)) % 4 == 1:
                        self.collector.turnLeft()
                    elif (self.collector.state.rotation - self.cords_to_rotation(self.collector.state.position, step)) % 4 == 3:
                        self.collector.turnRight()
                    elif (self.collector.state.rotation - self.cords_to_rotation(self.collector.state.position, step)) % 4 == 2:
                        self.collector.turnRight()
                        self.collector.turnRight()
                    self.update()
                    if not path:
                        break
            self.empty_bin(step)
            self.update()

    def DoPossibleMove(self, direction):
        return direction

##################################################################### DFS
    def mark_as_visited(self, grid, pos):
        for x, y in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if 0 <= x < self.gridWidth and 0 <= y < self.gridHeight and isinstance(grid[y][x], Bin):
                grid[y][x].visited = True
        return grid

    def empty_bin(self, pos):
        for x, y in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if 0 <= x < self.gridWidth and 0 <= y < self.gridHeight and isinstance(self.grid[y][x], Bin):
                self.grid[y][x].empty()

    def end_conditions(self, grid):
        for i in range(0, self.gridHeight):
            for obj in grid[i]:
                if isinstance(obj, Bin):
                    if not obj.visited: return False
        return True

    def bfs_wrapper(self, grid, pos):
        while True:
            self.results.append(self.bfs(grid, pos))
            pos = self.results[-1][-1]
            grid = self.mark_as_visited(grid, pos)
            if self.end_conditions(grid):
                break

    def bfs(self, grid, start):
        queue = collections.deque([[start]])
        seen = [[start]]
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self.break_conditions(grid, [x, y]):
                return path
            for x2, y2 in ((x+1, y), (x-1, y), (x, y-1), (x, y+1)):
                if 0 <= x2 < self.gridWidth and 0 <= y2 < self.gridHeight and isinstance(grid[y2][x2], Road) and (x2, y2) not in seen:
                    queue.append(path + [[x2, y2]])
                    seen.append((x2, y2))

    def break_conditions(self, grid, pos):
        for x, y in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if 0 <= x < self.gridWidth and 0 <= y < self.gridHeight and isinstance(grid[y][x], Bin):
                if not grid[y][x].visited: return True
        return False

    def cords_to_rotation(self, collector_position, next_step):
        rotation = collector_position[0]-next_step[0], collector_position[1]-next_step[1]
        if rotation == (1, 0): return 3
        if rotation == (0, 1): return 0
        if rotation == (-1, 0): return 1
        if rotation == (0, -1): return 2
