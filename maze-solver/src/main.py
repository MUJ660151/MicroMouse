import pygame
import sys
from objects.maze import Maze
from objects.player import Player
from objects.solver import Solver

filepath = 'maze-solver/src/maps/94japan.txt'
playerImg = 'maze-solver/bluecreep.png'

if __name__ == "__main__":
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

    pygame.display.flip()

    solver = Solver()

    while running:
        
        '''events()
        loop()
        render()
        
        sensor()
        planner()
        actuator()
        render()'''
        
        time_passed = clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        solver.floodfill()
        currentPos = (sprite.y, sprite.x)
        neighbours = solver.get_neighbours(currentPos[0], currentPos[1])
        angle = sprite.get_angle_offset(solver.array[currentPos[0]][currentPos[1]], neighbours)
        sprite.rotate_on_center(angle)
        sprite.move_forward()
        if solver.array[sprite.y][sprite.x][0] == 0:
            if solver.target == solver.center:
               solver.set_goal([solver.startCoords])
            elif solver.target == [solver.startCoords]:
                solver.set_goal(solver.center)
        solver.reset_array_vals()

    pygame.quit()
    sys.exit()


#TODO fix the wrong val getting changed movementfor row in self.array: