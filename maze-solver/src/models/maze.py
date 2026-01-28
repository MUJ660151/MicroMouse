import pygame
import sys

class Maze:
    CELL_SIZE = 25
    WALL_COLOR = (0, 0, 0)
    PATH_COLOR = (255, 255, 255)
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 480
    WALL_WIDTH = 5

    def __init__(self, filename,screen):
        self.wallList = []
        self.MAZE_DATA = self.__txt_to_list(filename)
        self.WIDTH = len(self.MAZE_DATA[0]) *Maze.CELL_SIZE
        self.HEIGHT = len(self.MAZE_DATA) *Maze.CELL_SIZE
        self.pathVal = ' '
        self.background = self.draw_maze(screen)

    def __txt_to_list(self, filename):
        array = []
        with open(filename) as f:
            line = f.readline()
            while line != '':
                line = line.strip()
                array.append(list(line))
                line = f.readline()
            f.close()
        return array
    def get_center_tiles(self):
        return [self.MAZE_DATA[self.goalPos[1]-1][self.goalPos[0]-1],
        self.MAZE_DATA[self.goalPos[1]+1][self.goalPos[0]-1],
        self.MAZE_DATA[self.goalPos[1]-1][self.goalPos[0]+1],
        self.MAZE_DATA[self.goalPos[1]+1][self.goalPos[0]+1]]
    
    def draw_maze(self, screen):
        screen.fill(Maze.PATH_COLOR)
        wallsUp = 0
        tilesUp = 0

        for y, row in enumerate(self.MAZE_DATA):
            wallsLeft = 0
            tilesLeft = 0
            for x, col in enumerate(row):
                posX = wallsLeft*Maze.WALL_WIDTH + tilesLeft*Maze.CELL_SIZE
                posY = wallsUp*Maze.WALL_WIDTH + tilesUp*Maze.CELL_SIZE
                if y %2 == 0:
                    rWidth = Maze.WALL_WIDTH
                else:
                    rWidth = Maze.CELL_SIZE
                if x % 2== 0:
                    rHeight = Maze.WALL_WIDTH
                    wallsLeft += 1
                else:
                    rHeight = Maze.CELL_SIZE
                    tilesLeft += 1
                if col == self.pathVal:
                    pygame.draw.rect(screen, Maze.PATH_COLOR, ((posX, posY), (rHeight, rWidth)))
                elif col != 'S':# and col != 'G':
                    pygame.draw.rect(screen, Maze.WALL_COLOR, ((posX, posY), (rHeight, rWidth)))
                    self.wallList.append((posX, posY))
                    if col == 'G':
                        self.goalPos = (x,y)
                """else:
                    print("unrecognized character", x, y)"""
            if y %2==0:
                wallsUp += 1
            else:
                tilesUp += 1
