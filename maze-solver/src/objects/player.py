import pygame
from objects.maze import Maze
import sys
import math 
from objects.solver import Solver

class MouseCrashedError(Exception):
    pass
class Player(Maze, pygame.sprite.Sprite):
    stepVal = Maze.WALL_WIDTH+Maze.CELL_SIZE
    halfStepVal = Maze.WALL_WIDTH+Maze.CELL_SIZE/2
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def __init__(self, x, y, image):
        
        self.speed = 0
        self.rotation = 0
        self.x = x*2+1#*Player.stepVal +Player.halfStepVal # col
        self.y = y*2+1#*Player.stepVal +Player.halfStepVal# row
        self.OG_IMAGE = pygame.image.load(image).convert_alpha()
        self.image = self.OG_IMAGE
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect().move(x*Player.stepVal+10, y*Player.stepVal+10)

    """def blitme(self, prev): # dirty = [all prev]
        self.screen.blit(self.background, prev, prev)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update([prev, self.rect])"""

    def check_wall(self, orOffset=0, distance=halfStepVal):
        future_rect = self.rect.copy()
        tdir = math.radians(self.rotation + 90*orOffset)
        dx = math.cos(tdir)*distance
        dy = -(math.sin(tdir)*distance)
        future_rect.x += dx
        future_rect.y += dy

        if future_rect.collidelist(self.maze.wallList) != -1:
            return True
        return False

    def move_forward(self, distance=stepVal):
        old_rect = self.rect.copy()
        dx, dy = 0,0
        if self.check_wall():
            raise MouseCrashedError 
        else:
            tdir = math.radians(self.rotation)
            dx = math.cos(tdir)
            dy = -(math.sin(tdir))
            self.x += int(dx)*2
            self.y += int(dy)*2
            self.rect.x += dx*distance
            self.rect.y += dy*distance
            self.blitme(old_rect)

    
    def get_next_tile(self, current, neighbours):
        valid_moves = []
        if current[1] == 0: # is not visited previously
            if self.check_wall():    #check and set walls
                current[2][self.offsets[0]] = 1    #TODO MAKE SURE THIS UPDATES IN CORRECT NAMESPACE
                neighbours[self.offsets[0]][2][self.offsets[2]] = 1
            else:
                valid_moves.append(self.offsets[0])
            if self.check_wall(1):
                current[2][self.offsets[1]] = 1
                neighbours[self.offsets[1]][2][self.offsets[3]] = 1
            else:
                valid_moves.append(self.offsets[1]) 
            if self.check_wall(2):
                current[2][self.offsets[2]] = 1
                neighbours[self.offsets[2]][2][self.offsets[0]] = 1
            else:
                valid_moves.append(self.offsets[2])
            if self.check_wall(3):
                current[2][self.offsets[3]] = 1
                neighbours[self.offsets[3]][2][self.offsets[1]] = 1
            else:
                valid_moves.append(self.offsets[3])
        else:
            if current[2][0] == 0:
                valid_moves.append(0)
            if current[2][1] == 0:
                valid_moves.append(1)
            if current[2][2] == 0:
                valid_moves.append(2)
            if current[2][3] == 0:
                valid_moves.append(3)

        
        
        #ccompare tiles in directions that have no walls
        #return tile with lowest val
        

    def rotate_on_center(self, angle):
        self.rotation = (self.rotation +angle) % 360
        self.offsets = [self.rotation%4, (self.rotation+1)%4,
            (self.rotation+2)%4, (self.rotation+3)%4]
        old_rect = self.rect.copy()
        self.image = pygame.transform.rotate(self.OG_IMAGE, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.blitme(old_rect)
        #return old_rect