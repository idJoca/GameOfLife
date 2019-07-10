import pygame
import pygame.gfxdraw
import numpy as np
import random
import math


class Main():
    _continue_flag = True
    ZOOM_STEPS = 3
    BACKGROUND_COLOR = (40, 40, 40)
    CELL_COLOR = (250, 250, 250)
    GRID_COLOR = (100, 100, 100)
    def __init__(self, width,
                 height,
                 resolution, fps=30):
        pygame.init()
        if (width == 0 or height == 0):
            self.set_fullscreen()
            self.fullscreen = True
        else:
            self.canvas = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.fullscreen = False
        self.canvas.fill(self.BACKGROUND_COLOR)
        # Sets the width and height
        screen_details = pygame.display.Info()
        self.width = screen_details.current_w
        self.height = screen_details.current_h
        self.fps = fps
        self.resolution = resolution
        self.initial_resolution = self.resolution

    def set_fullscreen(self):
        self.canvas = pygame.display \
                            .set_mode(
                                      (0, 0),
                                      pygame.FULLSCREEN)
        screen_details = self.canvas.get_size()
        self.width = screen_details[0]
        self.height = screen_details[1]
        print(screen_details)

    def create_grid(self):
        self.grid_state = np.random \
                            .randint(0,10,
                                     ((self.width // self.initial_resolution,
                                       self.height // self.initial_resolution)))
        self.grid_state = np.where(self.grid_state > 8, 1, 0)

    def start(self, _range=None):
        # Do Stuff
        self.create_grid()
        self.resolution = self.initial_resolution
        self.clock = pygame.time.Clock()

    def compute_cells(self, grid):
        nbrs_count = sum(np.roll(np.roll(grid, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
        # return (nbrs_count == 2) | (grid & (nbrs_count >= 1) & (nbrs_count <= 3)) Larabirint
        # return ((((nbrs_count == 1))) | (grid & ((nbrs_count == 1) | (nbrs_count == 2))))
        return ((((nbrs_count == 3))) | (grid & ((nbrs_count == 2)))) # Normal

    def animate(self):
        self.grid_state = self.compute_cells(self.grid_state)
        grid_state_index = self.grid_state.nonzero()
        if (len(grid_state_index[0]) > 0):
            self.vectorized_draw(grid_state_index[0], grid_state_index[1])

    def redraw(self):
        grid_state_index = self.grid_state.nonzero()
        if (len(grid_state_index[0]) > 0):
            self.vectorized_draw(grid_state_index[0], grid_state_index[1])

    def hand_draw(self, x, y):
        i = x // self.resolution
        j = y // self.resolution
        self.grid_state[i][j] = 1
    
    def hand_undraw(self, x, y):
        i = x // self.resolution
        j = y // self.resolution
        self.grid_state[i][j] = 0

    def draw(self, i, j):
        """radius = self.resolution//2
        pygame.draw.circle(self.canvas,
                           self.CELL_COLOR,
                           (i * self.resolution + radius,
                           j * self.resolution + radius),
                           radius)"""
        pygame.draw.rect(self.canvas,
                         self.CELL_COLOR,
                         pygame.Rect((i * self.resolution,j * self.resolution),
                         (self.resolution, self.resolution)),0)
    
    def draw_row_lines(self, row):
        lines = ((0, row), (self.width, row))
        pygame.draw.aalines(self.canvas,
                          self.GRID_COLOR,
                          0,
                          lines)

    def draw_col_lines(self, col):
        lines = ((col, 0), (col, self.height))
        pygame.draw.aalines(self.canvas,
                          self.GRID_COLOR,
                          0,
                          lines)

    def move_screen(self, left,
                    right,
                    up,
                    down):
        if (left):
            step = math.ceil(self.initial_resolution / self.resolution)
            self.grid_state = np.roll(self.grid_state, step, 0)
        if (right):
            step = math.ceil(self.initial_resolution / self.resolution)
            self.grid_state = np.roll(self.grid_state, -step, 0)
        if (up):
            step = math.ceil(self.initial_resolution / self.resolution)
            self.grid_state = np.roll(self.grid_state, step, 1)
        if (down):
            step = math.ceil(self.initial_resolution / self.resolution)
            self.grid_state = np.roll(self.grid_state, -step, 1)
        self.canvas.fill(self.BACKGROUND_COLOR)
        self.redraw()

    def loop(self):
        self.vectorized_draw = np.vectorize(self.draw)
        vectorized_draw_row_lines = np.vectorize(self.draw_row_lines)
        vectorized_draw_col_lines = np.vectorize(self.draw_col_lines)
        paused = False
        draw_button_down = False
        undraw_button_down = False
        left, right, up, down = [False] * 4
        while self._continue_flag is True:
            # Change
            self.move_screen(left, right, up, down)
            if (not paused):
                self.canvas.fill(self.BACKGROUND_COLOR)
                self.animate()
            else:
                # Draw lines:
                cols = np.arange(0, self.width, self.resolution)
                rows = np.arange(0, self.height, self.resolution)
                vectorized_draw_row_lines(rows)
                vectorized_draw_col_lines(cols)
            pygame.display.flip()
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                # Quit the program if the use close the windows
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    self._continue_flag = False
                # Or press ESCAPE
                if (event.type == pygame.KEYUP):
                    if (event.key == pygame.K_LEFT):
                        left = False
                    if (event.key == pygame.K_RIGHT):
                        right = False
                    if (event.key == pygame.K_UP):
                        up = False
                    if (event.key == pygame.K_DOWN):
                        down = False
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        self._continue_flag = False
                    if (event.key == pygame.K_SPACE):
                        paused = not paused
                    if (event.key == pygame.K_DELETE):
                        self.canvas.fill(self.BACKGROUND_COLOR)
                        paused = True
                        self.grid_state.fill(0)
                    if (event.key == pygame.K_r):
                        paused = False
                        self.start()
                    if (event.key == pygame.K_LEFT):
                        left = True
                    if (event.key == pygame.K_RIGHT):
                        right = True
                    if (event.key == pygame.K_UP):
                        up = True
                    if (event.key == pygame.K_DOWN):
                        down = True
                    if (event.key == pygame.K_F11):
                        if (self.fullscreen is False):
                            self.fullscreen = True
                            pygame.display.quit()
                            pygame.display.init()
                            self.set_fullscreen()
                        else:
                            self.fullscreen = False
                            self.canvas = pygame.display.set_mode((self.width, self.height),
                                                          pygame.RESIZABLE)
                    if (event.key == pygame.K_z):
                        self.canvas.fill(self.BACKGROUND_COLOR)
                        self.animate()
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if (event.button == 4):
                        x,y = event.pos
                        self.resolution += self.ZOOM_STEPS
                        ratio = (self.resolution - self.ZOOM_STEPS) / self.resolution
                        new_width = (self.width - self.width * ratio) * x
                        new_height = (self.height - self.height * ratio) * y
                        normalization_width = (self. resolution * self.width)
                        normalization_height = (self. resolution * self.height)
                        self.grid_state = np.roll(self.grid_state,
                                                  -int(new_width) //
                                                  normalization_width, 0)

                        self.grid_state = np.roll(self.grid_state,
                                                  -int(new_height) //
                                                  normalization_height, 1)
                        if (paused):
                            self.canvas.fill(self.BACKGROUND_COLOR)
                            self.redraw()
                    elif (event.button == 5):
                        x,y = event.pos
                        if (self.resolution > self.initial_resolution):
                            self.resolution -= self.ZOOM_STEPS
                            ratio = (self.resolution) / (self.resolution + self.ZOOM_STEPS)
                            new_width = (self.width - self.width * ratio) * x
                            new_height = (self.height - self.height * ratio) * y
                            normalization_width = (self. resolution * self.width)
                            normalization_height = (self. resolution * self.height)
                            self.grid_state = np.roll(self.grid_state,
                                                      int(new_width) //
                                                      normalization_width, 0)

                            self.grid_state = np.roll(self.grid_state,
                                                      int(new_height) //
                                                      normalization_height, 1)
                            if (paused):
                                self.canvas.fill(self.BACKGROUND_COLOR)
                                self.redraw()
                    if (event.button == 3):
                        undraw_button_down = True
                        x, y = event.pos
                        self.hand_undraw(x, y)
                    if (event.button == 1):
                        draw_button_down = True
                        x, y = event.pos
                        self.hand_draw(x, y)
                if (event.type == pygame.MOUSEBUTTONUP):
                    if (event.button == 1):
                        draw_button_down = False
                    if (event.button == 3):
                        undraw_button_down = False
                if (event.type == pygame.MOUSEMOTION):
                    if (draw_button_down is True):
                        x, y = event.pos
                        self.hand_draw(x, y)
                    if (undraw_button_down is True):
                        x, y = event.pos
                        self.hand_undraw(x, y)
                if (event.type == pygame.VIDEORESIZE):
                    self.width, self.height = event.size
                    self.grid_state.resize((self.width // self.resolution,
                                           self.height // self.resolution), refcheck=False)
                    if (not self.fullscreen):
                        self.canvas = pygame.display.set_mode((self.width, self.height),
                                                          pygame.RESIZABLE)
main = Main(0, 0, 5)
main.start()
main.loop()