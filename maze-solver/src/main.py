import pygame
import sys
from models.maze import Maze
from models.player import Player


class App:
    def __init__(self):
        self._running = True
        self._display = None
        self.size = self.weight, self.height = 480, 480

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode(self.size, pygame.RESIZABLE | pygame.SCALED)
        self._running = True
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_cleanup():
        pygame.quit()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
"""
if __name__ == "__main__":
    theApp = App()
    theApp.onExecute
"""

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
#maze.draw_maze(background) 

sprite = Player(6, 6, playerImg, screen, maze, background)
screen.blit(background, (0,0))
screen.blit(sprite.image, sprite.rect)
maze.set_wall(1, 13, screen, 0)
pygame.display.flip()
while running:
    """
    events()
    loop()
    render()
    """
    time_passed = clock.tick(2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not sprite.check_wall():
        sprite.move_forward()
    else:
        sprite.rotate_on_center(90)


    


pygame.quit()
sys.exit()