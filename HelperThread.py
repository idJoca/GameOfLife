from graphics import *
import random
import copy
import time
import threading
#Rules:
"""
(cell[i] = 1) < 2 neighbors or > 3 neighbors = 0
(cell[i] = 0) == 3 neighbors = 1
"""
class MyThread(threading.Thread):

    cols = 0
    rows = 0
    grid = []
    newGrid = []
    rects = []
    win = None
    def __init__(self, cols, rows, grid, newGrid):        
        threading.Thread.__init__(self)
        self.cols = cols
        self.rows = rows
        self.grid = grid
        self.newGrid = newGrid

    def getEdge(self, coord, planeLimit, direction):
        return int((coord + direction + planeLimit) % planeLimit)

    def evaluateNeighbors(self, x, y, gridon):
        #neighbors = []
        neighborsAlive = 0
        for i in range(-1, 2):          
            newX = self.getEdge(x, self.cols, i)      
            for j in range(-1, 2):
                if (i == 0 and j == 0): continue
                newY = self.getEdge(y, self.rows, j)
                #neighbors.append([newX, newY])
                neighborsAlive += gridon[newX][newY]
        return neighborsAlive

    """def DecideToShow(self, state, rect):
        for j in range(0, (self.rows)):      
            if(state == 1 and (rect.canvas == None)):                   
                rect.setFill("white")
                rect.draw(self.win)
            elif(not(state == 1) and rect.canvas != None):
                rect.undraw()"""

    def run(self):  
        #time.sleep(2)
        """for i in range(0, (self.cols)):          
            for j in range(0, (self.rows)):  
                state = self.grid[i][j]      
                rect =  self.rects[i][j]        
                self.DecideToShow(state, rect) """              
        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.neighborsAlive = self.evaluateNeighbors(i, j, self.grid)
                if(self.grid[i][j] == 1 and (self.neighborsAlive < 2 or self.neighborsAlive > 3)):
                    self.newGrid[i][j] = 0
                elif(not(self.grid[i][j] == 1) and self.neighborsAlive == 3):
                    self.newGrid[i][j] = 1
        #print(grid == newGrid)    

