import pygame
import sys
from objects.maze import Maze
from objects.player import Player
from objects.solver import Solver

filepath = 'maze-solver/src/maps/94japan.txt'
playerImg = 'maze-solver/bluecreep.png'


def convert_millis(milliseconds):
    # 1. Calculate total seconds and remaining milliseconds
    total_seconds, remaining_ms = divmod(milliseconds, 1000)
    
    # 2. Calculate minutes and remaining seconds
    minutes, seconds = divmod(total_seconds, 60)
    
    return f"{minutes}:{seconds}.{remaining_ms}"
def blitSpot(background, image, image_rect):
    #screen.blits([(background, image_rect),(image, image_rect)])
    screen.blit(background, image_rect, image_rect)
    screen.blit(image, image_rect)
    pygame.display.update(image_rect)


if True or __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    start_time = None
    running = True
    game_active = True

    screen = pygame.display.set_mode((Maze.SCREEN_WIDTH, Maze.SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    maze = Maze(filepath, background)

    sprite = Player(0, 15, playerImg, screen, maze, background)
    
    screen.blit(background, (0,0))
    screen.blit(sprite.image, sprite.rect)

    FONT = pygame.font.Font(None, 30)

    #renders lap times to screen
    """text_surface = FONT.render("00:00.00", True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (10, 10)
    screen.blit(text_surface, text_rect)

    text_surface2 = FONT.render("00:00.00", True, (255, 0, 0))
    text_rect2 = text_surface2.get_rect()
    text_rect2.topleft = (10, 40)
    screen.blit(text_surface2, text_rect2)

    text_surface3 = FONT.render("00:00.00", True, (255, 0, 0))
    text_rect3 = text_surface3.get_rect()
    text_rect3.topleft = (10, 70)
    screen.blit(text_surface3, text_rect3)"""

    pygame.display.flip()

    solver = Solver()
    loops = 0
    while running:
        
        '''events()
        loop()
        render()
        
        sensor()
        planner()
        actuator()
        render()'''
        
        time_passed = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game_active:
            solver.floodfill()
            currentPos = (sprite.y, sprite.x)
            neighbours = solver.get_neighbours(currentPos[0], currentPos[1])
            angle = sprite.get_angle_offset(solver.array[currentPos[0]][currentPos[1]], neighbours)
            sprite.rotate_on_center(angle)
            sprite.move_forward()

            if solver.array[sprite.y][sprite.x][0] == 0:
                if loops <2:
                    if solver.target == solver.center: #completed first run to center
                        solver.set_goal([solver.startCoords])
                        loops +=1
                        ms = pygame.time.get_ticks()
                        print(convert_millis(ms))
                    elif solver.target == [solver.startCoords]: # completed return to start
                        solver.set_goal(solver.center)
                        loops+=1
                        ms2 = pygame.time.get_ticks() -ms
                        print(convert_millis(ms2))
                else:
                    game_active = False
                    ms3 = pygame.time.get_ticks() - ms - ms2
                    print(convert_millis(ms3))
            solver.reset_array_vals()


            #renders lap times to screens
            """if loops == 0:
                ms = pygame.time.get_ticks()
                text_surface = FONT.render(str(convert_millis(ms)), True, (255, 0, 0))
                blitSpot(background, text_surface, text_rect)
            elif loops ==1:
                ms2 = pygame.time.get_ticks() - prev_time
                text_surface2 = FONT.render(str(convert_millis(ms2)), True, (255, 0, 0))
                blitSpot(background, text_surface2, text_rect2)
            elif loops ==2:
                ms3 = pygame.time.get_ticks() - prev_time
                text_surface3 = FONT.render(str(convert_millis(ms3)), True, (255, 0, 0))
                blitSpot(background, text_surface3, text_rect3)"""

    pygame.quit()
    sys.exit()