import pygame
import sys
from objects.maze import Maze
from objects.player import Player
from objects.solver import Solver

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 480, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE | pygame.SCALED)
        filepath = 'maze-solver/src/maps/94japan.txt'
        playerImg = 'maze-solver/bluecreep.png'
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.maze = Maze(filepath, self.background)
        self.player = Player(0, 15, playerImg)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()

        self.clock = pygame.time.Clock()
        self.running = True
    def on_loop(self):
        
        pass
    def run(self):
        while self.running:
            self.time_passed = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()
        sys.exit()

    def update_screen(self):
        self.screen.blit(self.background, prev, prev)
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update([prev, self.rect])

if __name__ == "__main__":
    g = Game()
    g.run()