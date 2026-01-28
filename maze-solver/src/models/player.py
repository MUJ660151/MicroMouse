import pygame
from models.maze import Maze
import sys
import math 

class MouseCrashedError(Exception):
    pass
class Player(pygame.sprite.Sprite, Maze):
    stepVal = Maze.WALL_WIDTH+Maze.CELL_SIZE
    halfStepVal = Maze.WALL_WIDTH+Maze.CELL_SIZE/2
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def __init__(self, x, y, image, screen, maze, background):
        self.background = background
        self.maze = maze
        self.array = maze.MAZE_DATA
        self.screen = screen
        self.speed = 0
        self.rotation = 0
        self.orientaion = 0
        self.x = x*2+1#*Player.stepVal +Player.halfStepVal # col
        self.y = y*2+1#*Player.stepVal +Player.halfStepVal# row
        self.OG_IMAGE = pygame.image.load(image).convert_alpha()
        self.image = self.OG_IMAGE
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect().move(x*Player.stepVal+10, y*Player.stepVal+10)#x*Player.stepVal+Player.halfStepVal-self.w/2, \
            #y*Player.stepVal+Player.halfStepVal-self.h/2)#self.x-self.w/2,self.y-self.h/2)

    def blitme(self, prev): # dirty = [all prev]
        print(self.background)
        self.screen.blit(self.background, prev, prev)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update([prev, self.rect])

    def check_wall(self, orOffset=0, distance=stepVal):
        future_rect = self.rect.copy()
        tdir = self.rotation + 90*orOffset
        if tdir > 360:
            tdir -= 360
        elif tdir < 0:
            tdir+= 360
        dx = math.sin(tdir)*distance
        dy = math.cos(tdir)*distance
        future_rect.x += dx
        future_rect.y += dy

        if future_rect.collidelist(self.maze.wallList) != -1:
            return True
        return False
        
    def wall_front(self):
        return self.check_wall()
    def wall_right(self):
        return self.check_wall(1)
    def wall_back(self):
        return self.check_wall(2)
    def wall_left(self):
        return self.check_wall(3)

    def get_pos(self):
        return self.x*Player.stepVal+10, self.y*Player.stepVal+10
    def move_forward(self, distance=stepVal):
        old_rect = self.rect.copy()
        if self.check_wall():
            raise MouseCrashedError 
        """if self.rotation == 0:
            if self.array[self.y][self.x+1] == ' ':
                self.x += 2
                self.rect.x+= distance
            else:
                print("mouse crashed")
        elif self.rotation ==90:
            if self.array[self.y+1][self.x] == ' ':
                self.y += 2
                self.rect.y+= distance
            else:
                print("mouse crashed")
        elif self.rotation == 180:
            if self.array[self.y][self.x-1] == ' ':
                self.x -= 2
                self.rect.x-= distance
            else:
                print("mouse crashed")
        elif self.rotation == 270:
            if self.array[self.y-1][self.x] == ' ':
                self.y -= 2
                self.rect.y-= distance
            else:
                print("mouse crashed")
        else:
            self.rotate_on_center(-self.rotation)
        self.blitme(old_rect)"""
        

    def rotate_on_center(self, angle):
        #gets distorted if not multiple of 90
        self.rotation = (self.rotation +angle) % 360
        self.orientaion = int(self.rotation/45)
        old_rect = self.rect.copy()
        self.image = pygame.transform.rotate(self.OG_IMAGE, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.blitme(old_rect)