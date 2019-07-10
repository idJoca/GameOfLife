# Using:
Just download this repo and run the 'main.py' file.
Please, ignore the other files, such as 'main2.py', 'HelperThread.py' or even, 'test.cprof'
You also need to have installed 'pygame' and 'numpy'. Both of which can be installed via:
```
pip install pygame

pip install numpy
```
# GameOfLife
The Game of Life, also known simply as Life,
is a cellular automaton devised by the British mathematician John Horton Conway in 1970.

The game is a zero-player game,
meaning that its evolution is determined by its initial state,
equiring no further input.
One interacts with the Game of Life by creating an initial configuration and observing how it evolves,
or, for advanced players, by creating patterns with particular properties.
> https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

# Version 2.0
## Improved performance issues:
- Now using, numpy arrays, with broadcasting and vectorization. 
- Changed the graphics library from, tkinter to pygame, a more specialized library for this kind of application.
## Added new controls:
- **Spacebar** to pauses the simulation and goes into 'edit' mode.
- **R** key resets the simulation.
- The **arrow keys** controls the camera.
- The **left mouse key** puts a cell.
- The **right mouse key** deletes a cell.
- The **scroll wheel** changes the zoom.
- The **Z** key goes one frame at a time.
- The **F11** key toggles the fullscreen mode
