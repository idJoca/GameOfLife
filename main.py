from graphics import *
import random
import copy
import time
from joblib import Parallel, delayed
from HelperThread import MyThread
#Rules:
"""
(cell[i] = 1) < 2 neighbors or > 3 neighbors = 0
(cell[i] = 0) == 3 neighbors = 1
"""

width = 850
height = 600
resolution = 8
cols = int(width / resolution)
rows = int(height / resolution)
grid = []
rects = []
def createGrid(win):  
    random.seed()        
    for i in range(0, (cols)):        
            x = i * resolution
            grid.append([])
            rects.append([])
            for j in range(0, (rows)):     
                y = j * resolution      
                color = random.randint(0, 6)                
                if (color == 1):
                    grid[i].append(color)   
                else:
                    grid[i].append(0)   
                rects[i].append(Rectangle(Point(x, y), Point(x + resolution-1, y + resolution-1)))
                rects[i][j].setOutline("white")  
                rects[i][j].config["fill"] = "white"               
                rects[i][j].draw(win)       

def getEdge(coord, planeLimit, direction):
    return int((coord + direction + planeLimit) % planeLimit)

def evaluateNeighbors(x, y, gridon):
    #neighbors = []
    neighborsAlive = 0
    for i in range(-1, 2):          
        newX = getEdge(x, cols, i)      
        for j in range(-1, 2):
            if (i == 0 and j == 0): continue
            newY = getEdge(y, rows, j)
            #neighbors.append([newX, newY])
            neighborsAlive += gridon[newX][newY]
    return neighborsAlive

def DecideToShow(state, rect):
    for j in range(0, (rows)):      
        if(state == 1 and (rect.canvas == None)):                   
            rect.setFill("black")
            rect.draw(win)
        elif(not(state == 1) and rect.canvas != None):
            rect.undraw()

win = GraphWin("GameOfLife", width, height)
win.setBackground("white")

createGrid(win)


#list(map(lambda x: list(map(lambda y: y.draw(), x)), grid))

newGrid = copy.deepcopy(grid)

while(True):     
    for i in range(0, (cols)):          
        #concat = (grid[i], rects[i])
        #Parallel(n_jobs=-1, verbose=verbosity_level, backend="multiprocessing")(map(delayed(myfun), cno)) 
        for j in range(0, (rows)):  
            neighborsAlive = evaluateNeighbors(i, j, grid)
            state = grid[i][j]      
            rect =  rects[i][j]     
            if(state == 1):
                if((rect.config["fill"] != "black")) :              
                    rect.config["fill"] = "black" 
                    rect.canvas.itemconfig(rect.id, rect.config)  
                    rect.canvas.flush()
                if((neighborsAlive < 2 or neighborsAlive > 3)):
                    newGrid[i][j] = 0
            else:
                if(rect.config["fill"] != "white"):
                    rect.config["fill"] = "white" 
                    rect.canvas.itemconfig(rect.id, rect.config)  
                    rect.canvas.flush()
                if(neighborsAlive == 3):
                    newGrid[i][j] = 1
            #win.redraw()               
            
    #print(grid == newGrid)    
            
    grid = copy.deepcopy(newGrid)
    #time.sleep(0.7)
