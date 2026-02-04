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
        self.sprite = Player(0, 15, playerImg)
        self.solver = Solver()
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.sprite.image, self.sprite.rect)
        pygame.display.flip()

        self.clock = pygame.time.Clock()
        self.running = True

    def on_loop(self):
        self.solver.floodfill()
        neighbours = self.solver.get_neighbours()
        #add self.x and self.y updates
        angle = self.sprite.get_angle_offset((self.x, self.y), neighbours)
        self.sprite.rotate_on_center(angle)
        pass
        
    def run(self):
        while self.running:
            self.time_passed = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.solver.floodfill()
            currentPos = (self.sprite.y, self.sprite.x)
            neighbours = self.solver.get_neighbours(currentPos[0], currentPos[1])
            angle = self.sprite.get_angle_offset(self.solver.array[currentPos[0]][currentPos[1]], neighbours)
            self.sprite.rotate_on_center(angle)
            self.sprite.move_forward()
        pygame.quit()
        sys.exit()

    def update_screen(self, dirty, new):
        self.screen.blit(self.background, dirty, dirty)
        self.screen.blit(new, (new.rect.x, new.rect.y))
        pygame.display.update([dirty, new.rect])

if __name__ == "__main__":
    g = Game()
    g.run()