from collections import deque
from objects.player import Player
class Solver:
    directions = [(0, 2, -1, 0), (1, 3,0,1), (2, 0,1,0), (3, 1, 0, -1)]
    def __init__(self, player, startCoords=(0,15)):
        self.player = player
        self.width, self.height = 16, 16 #make size adaptable
        self.startCoords = startCoords
        self.center = ((7,7), (7,8), (8,7), (8,8)) #make size adaptable
        self.target = self.center
        self.array = [[[512, 0, [0,0,0,0]] for x in range(16)] for y in range(16)]
        self.set_goal()
        #dist from center, visited, walls NESW

    def reset_array_vals(self, target=None):
        for r in len(self.array):
            for c in len(self.array[r]):
                self.array[r][c][0] = 512
        if target is not None:
            self.set_goal(target)
    
    def set_goal(self, target=None):
        if target is not None:
            self.target = target
        if len(target) == 4:
            self.array[self.target[0][0]][self.target[0][1]][0] = 0
            self.array[self.target[1][0]][self.target[1][1]][0] = 0
            self.array[self.target[2][0]][self.target[2][1]][0] = 0
            self.array[self.target[3][0]][self.target[3][1]][0] = 0
        else:
            self.array[self.target[0]][self.target[1]][0] = 0

    def floodfill(self):
        visited_in_loop = [[False for c in range(self.width)] for r in range(self.height)]
        queue = deque(self.target)
        while queue:
            r,c = queue.popleft()
            for nC, nN, dr, dc in Solver.directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.width and 0 <= nc < self.height and self.array[nr][nc][0] > self.array[r][c][0]+1:
                    if not visited_in_loop[nr][nc]:
                        if self.array[nr][nc][2][nN] == 0 and self.array[r][c][2][nC] == 0:
                            self.array[nr][nc][0] = self.array[r][c][0] + 1
                            queue.append((nr, nc))
                            visited_in_loop[nr][nc] = True
                        elif self.array[nr][nc][2][nN] != self.array[r][c][2][nC]: #if wall doesnt have coresponding wall in next cell
                            self.array[nr][nc][2][nN] = 1 # make wall true on both cells
                            self.array[r][c][2][nC] = 1
        for row in self.array:
            for col in row:
                print(col[0], end = " ")
            print()
    
    def set_wall(self):
        pass
        
    def get_neighbours(self, r, c):
        return self.array[r-1][c], self.array[r][c+1],self.array[r+1][c],self.array[r][c-1]
    
if __name__ == "__main__":
    s = Solver()

    s.floodfill()