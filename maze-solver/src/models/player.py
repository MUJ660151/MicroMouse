import pygame
from models.maze import Maze
import sys
class Player(pygame.sprite.Sprite, Maze):
    stepVal = Maze.WALL_WIDTH+Maze.CELL_SIZE
    halfStepVal = Maze.WALL_WIDTH+Maze.CELL_SIZE/2
    def __init__(self, x, y, image, screen, maze):
        self.array = maze
        self.screen = screen
        self.speed = 0
        self.rotation = 0
        self.x = x*2+1#*Player.stepVal +Player.halfStepVal # col
        self.y = y*2+1#*Player.stepVal +Player.halfStepVal# row
        self.image = pygame.image.load(image).convert_alpha()
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect().move(x*Player.stepVal+10, y*Player.stepVal+10)#x*Player.stepVal+Player.halfStepVal-self.w/2, \
            #y*Player.stepVal+Player.halfStepVal-self.h/2)#self.x-self.w/2,self.y-self.h/2)

    def blitme(self, prev, background):
        self.screen.blit(background, prev, prev)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update([prev, self.rect])

    def move_forward(self, distance=stepVal):
        #TODO make direction compatable
        if self.array[self.y+1][self.x] == ' ':
            self.x += 2
            self.rect.x+= distance
        else:
            print("mouse crashed")

    def rotate_on_center(self, angle, background):
        self.rotation+= angle
        if self.rotation > 360:
            self.rotation -= 360
        elif self.rotation < 0:
            self.rotation+= 360
        old_rect = self.rect.copy()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        #self.screen.blit(background, old_rect, old_rect)
        #self.screen.blit(self.image, new_rect)
        self.blitme(old_rect, background)