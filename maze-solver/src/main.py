import pygame
import sys
from objects.maze import Maze
from objects.player import Player
from objects.solver import Solver

filepath = 'maze-solver/src/maps/94japan.txt'
playerImg = 'maze-solver/bluecreep.png'
pygame.init()

clock = pygame.time.Clock()
running = True

screen = pygame.display.set_mode((Maze.SCREEN_WIDTH, Maze.SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
background = pygame.Surface(screen.get_size())
background = background.convert()

maze = Maze(filepath, background)

sprite = Player(0, 15, playerImg, screen, maze, background)

screen.blit(background, (0,0))
screen.blit(sprite.image, sprite.rect)

def loop():
    pass

pygame.display.flip()
while running:
    
    '''events()
    loop()
    render()
    
    sensor()
    planner()
    actuator()
    render()'''
    
    time_passed = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

print(time_passed)
    
pygame.quit()
sys.exit()
