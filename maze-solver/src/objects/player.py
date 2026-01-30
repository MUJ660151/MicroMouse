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
    sectors = [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]
    
    def __init__(self, x, y, image, screen, maze, background):
        self.maze = maze
        self.screen = screen
        self.background = background
        self.speed = 0
        self.rotation = 0
        self.orientation = 0
        self.x = x#*2+1#*Player.stepVal +Player.halfStepVal # col
        self.y = y#*2+1#*Player.stepVal +Player.halfStepVal# row
        self.OG_IMAGE = pygame.image.load(image).convert_alpha()
        self.image = self.OG_IMAGE
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect().move((x)*Player.stepVal+10, (y)*Player.stepVal+10)
        #self.offsets = [0, 1,2,3]

    def blitme(self, prev): # dirty = [all prev]
        self.screen.blit(self.background, prev, prev)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update([prev, self.rect])

    def check_wall(self, orOffset=0, distance=halfStepVal):
        future_rect = self.rect.copy()
        tdir = math.radians(self.rotation + 90*orOffset)
        dx = math.cos(tdir)*distance
        dy = math.sin(tdir)*distance
        future_rect.x += dx
        future_rect.y -= dy

        if future_rect.collidelist(self.maze.wallList) != -1:
            return True
        return False

    def move_forward(self, distance=stepVal):
        old_rect = self.rect.copy()
        dx, dy = 0,0
        if self.check_wall():
            raise MouseCrashedError 
        else:
            sI = int(((self.rotation +22.5)%360)/45)
            tdir = math.radians(self.rotation)
            dx = math.cos(tdir)
            dy = -(math.sin(tdir))
            #dx, dy = Player.sectors[sI]
            self.x += round(dx)
            self.y += round(dy)
            self.rect.x += round(dx*distance)
            self.rect.y += round(dy*distance)
            self.blitme(old_rect)

    #TODO ADD CHECKER FOR IF THE CURRENT TILE IS REAL
    def get_angle_offset(self, current, neighbours):#get_next_tile(self, current, neighbours):
        valid_moves = [] 
        self.offsets = [(self.orientation)%4, # of 90deg turns to face east
                        (self.orientation+1)%4, # of 90 deg turns to face north
                        (self.orientation+2)%4, # of 90 deg turns to face west
                        (self.orientation+3)%4] # of 90 deg turns to face south
        if current[1] == 0: # is not visited previously

            if neighbours[self.offsets[0]] is not None: #forward
                if self.check_wall():    #check and set walls
                    current[2][self.offsets[0]] = 1
                    neighbours[self.offsets[0]][2][self.offsets[2]] = 1
                else:
                    valid_moves.append(0)
            else:
                current[2][self.offsets[0]] = 1
            if neighbours[self.offsets[1]] is not None: #left
                if self.check_wall(1):
                    current[2][self.offsets[1]] = 1
                    neighbours[self.offsets[1]][2][self.offsets[3]] = 1
                else:
                    valid_moves.append(1) 
            else:
                current[2][self.offsets[1]] = 1
            if neighbours[self.offsets[2]] is not None:
                if self.check_wall(2):
                    current[2][self.offsets[2]] = 1
                    neighbours[self.offsets[2]][2][self.offsets[0]] = 1
                else:
                    valid_moves.append(2)
            else:
                current[2][self.offsets[2]] = 1
            if neighbours[self.offsets[3]] is not None:
                if self.check_wall(3):
                    current[2][self.offsets[3]] = 1
                    neighbours[self.offsets[3]][2][self.offsets[1]] = 1
                else:
                    valid_moves.append(3)
            else:
                current[2][self.offsets[3]] = 1
            current[1] = 1
        else:
            if current[2][self.offsets[0]] == 0 and neighbours[self.offsets[0]] is not None:
                valid_moves.append(0) 
            if current[2][self.offsets[1]] == 0 and neighbours[self.offsets[1]] is not None:
                valid_moves.append(1)
            if current[2][self.offsets[2]] == 0 and neighbours[self.offsets[2]] is not None: 
                valid_moves.append(2) 
            if current[2][self.offsets[3]] == 0 and neighbours[self.offsets[3]] is not None: 
                valid_moves.append(3) 
        lowest = 2048
        for move in valid_moves:
            if neighbours[self.offsets[move]][0] < lowest:
                lowest = neighbours[self.offsets[move]][0]
                next = move
            elif neighbours[self.offsets[move]][0] == lowest and neighbours[self.offsets[move]][1] == 0:
                next = move

                #next = self.offsets[move] #converts NESW to forward(0), right(1), backward(2), left(3)
        return 90*next #next
                #number of degrees to turn to get to target
        

    def rotate_on_center(self, angle): # counterclockwise
        self.rotation = (self.rotation +angle) % 360
        self.orientation = self.rotation // 90
        """self.offsets = [self.rotation%4, #relative to direction: forward
                        (self.rotation+1)%4, #                   right
                        (self.rotation+2)%4, #                   back
                        (self.rotation+3)%4] #                   left"""
        old_rect = self.rect.copy()
        self.image = pygame.transform.rotate(self.OG_IMAGE, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.blitme(old_rect)
        #return old_rect