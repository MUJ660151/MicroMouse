from collections import deque

class Solver:
    #directions = [(0, 2, -1, 0), (1, 3,0,1), (2, 0,1,0), (3, 1, 0, -1)]
    directions = [(1, 3,-1,0), (0, 2, 0, 1), (3, 1, 1, 0), (2, 0,0,-1)]
    def __init__(self, startCoords=(15,0)):
        #self.player = player
        self.width, self.height = 16, 16 #make size adaptable
        self.startCoords = startCoords
        self.center = ((7,7), (7,8), (8,7), (8,8)) #make size adaptable
        self.target = self.center
        self.array = [[[512, 0, [0,0,0,0]] for x in range(16)] for y in range(16)]
        self.set_goal()
        #dist from center, visited, walls NESW

    def reset_array_vals(self):
        for r in range(self.height):
            for c in range(self.width):
                self.array[r][c][0] = 512
        """if target is not None:
            self.target = target"""
        self.set_goal()
        
    
    def set_goal(self, target=None):
        if target is not None:
            self.target = target
        if len(self.target) == 4:
            self.array[self.target[0][0]][self.target[0][1]][0] = 0
            self.array[self.target[1][0]][self.target[1][1]][0] = 0
            self.array[self.target[2][0]][self.target[2][1]][0] = 0
            self.array[self.target[3][0]][self.target[3][1]][0] = 0
        else:
            self.array[self.target[0][0]][self.target[0][1]][0] = 0

    def floodfill(self):
        visited_in_loop = [[False for c in range(self.width)] for r in range(self.height)]
        queue = deque(self.target)
        while queue:
            r,c = queue.popleft()
            for nC, nN, dr, dc in Solver.directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.width and 0 <= nc < self.height:
                    if self.array[nr][nc][2][nN] != self.array[r][c][2][nC]:
                        self.array[nr][nc][2][nN] = 1
                        self.array[r][c][2][nC] = 1
                    if self.array[r][c][2][nC] == 0 and self.array[nr][nc][0] > self.array[r][c][0]+1:
                        #if not visited_in_loop[nr][nc]:
                            self.array[nr][nc][0] = self.array[r][c][0] + 1
                            queue.append((nr, nc))
                            visited_in_loop[nr][nc] = True
            
        """for row in self.array:
            for col in row:
                print(f"{col[0]:<2}", end = " ",)
            print()
        for row in self.array:
            for col in row:
                print("".join([str(x) for x in col[2]]), end= " ")
            print()"""
        
    def get_neighbours(self, r, c):
        neighbours = [None, None, None, None]
        if 0<=r-1<self.height:
            neighbours[1] = self.array[r-1][c]
        if 0<= c+1 < self.width:
            neighbours[0] = self.array[r][c+1]
        if 0 <=r+1< self.height:
            neighbours[3] = self.array[r+1][c]
        if 0<= c-1 < self.width:
            neighbours[2] = self.array[r][c-1]
        return neighbours
    
if __name__ == "__main__":
    s = Solver()

    s.floodfill()