from player import Player

class Movement(Player):
    def __init__(self):
        pass
    def move_forward(self, distance=Player.stepVal):
        self.rect.x+= distance