import pygame
import sys
from models.maze import Maze
from models.player import Player
filepath = 'maze-solver/src/maps/94japan.txt'
playerImg = 'maze-solver/bluecreep.png'
pygame.quit()
pygame.init()
clock = pygame.time.Clock()
running = True
screen = pygame.display.set_mode((Maze.SCREEN_WIDTH, Maze.SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
background = pygame.Surface(screen.get_size())
background = background.convert()
maze = Maze(filepath, background)
#maze.draw_maze(background) #MADE BACKGROUND ATTRIBUTE OF MAZE
pygame.display.flip()

sprite = Player(0, 15, playerImg, screen, maze.MAZE_DATA)
screen.blit(background, (0,0))
screen.blit(sprite.image, sprite.rect)

while running:
    time_passed = clock.tick(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    old_rect = sprite.rect.copy()
    sprite.move_forward()
    sprite.rotate_on_center(90, background)
    sprite.blitme(old_rect, background)


pygame.quit()
sys.exit()