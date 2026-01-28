import API
from collections import deque

class Maze:
    solution = []
    visited = []
    def __init__(self, height=16, width=16):
        self.height = height
        self.width = width
class Node:
    
    def __init__(self, data):
        self.data = data
        self.next = None
        self.visited = False




class Movement:
    pass