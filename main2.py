from tkinter import *
import random
import copy
import time
from HelperThread import MyThread
#Rules:
"""
(cell[i] = 1) < 2 neighbors or > 3 neighbors = 0
(cell[i] = 0) == 3 neighbors = 1
"""

width = 1200
height = 720
resolution = 15
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
                rects[i].append(win.create_rectangle(x, y, x + resolution -1, y + resolution -1, fill="white"))
                win.itemconfig(rects[i][j], outline="white")

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

def restart(arguments):
    global grid, rects, newGrid
    grid = []
    rects = []
    win.delete(ALL)
    createGrid(win)
    newGrid = copy.deepcopy(grid)

tk = Tk()
win = Canvas(tk, width=width, height=height)
tk.title("GameOfLife")
win.pack()
win.bind("<Button 1>", restart)
createGrid(win)

#list(map(lambda x: list(map(lambda y: y.draw(), x)), grid))

newGrid = copy.deepcopy(grid)

frameRate = 0
startTime = (time.perf_counter())
while(True):
    thread = MyThread(cols, rows, grid, newGrid)
    thread.start()
    for i in range(0, (cols)):          
        #concat = (grid[i], rects[i])
        #Parallel(n_jobs=-1, verbose=verbosity_level, backend="multiprocessing")(map(delayed(myfun), cno)) 
        for j in range(0, (rows)):  
            #thread = MyThread(cols, rows, grid, newGrid, i, j)
            #thread.start()
            state = grid[i][j]  
            rect =  rects[i][j]
            if(state == 1):
                if(win.itemcget(rect, "fill") != "black") :  
                    win.itemconfig(rect, fill='black')  
            else:
                if(win.itemcget(rect, "fill") != "white"):
                   win.itemconfig(rect, fill='white')            
    #tk.update()  
            #win.redraw()    
    #print(grid == newGrid) 
    thread.join() 
    win.update()   
    grid = copy.deepcopy(newGrid)
    frameRate += 1
    end = (time.perf_counter())
    if(end - startTime >= 1):        
        startTime = (time.perf_counter())
        print(frameRate)
        frameRate = 0
    #time.sleep(0.7)
