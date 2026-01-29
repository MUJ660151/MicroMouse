from player import Player
from maze import Maze
class Movement(Player):
    def __init__(self, maze, player):
        self.maze = maze
        self.player = player
        self.center_tiles = self.maze.get_center_tiles()
    def move_forward(self, distance=Player.stepVal):
        pass
    def get_neighbours(self, coord):
        pass