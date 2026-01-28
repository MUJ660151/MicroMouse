from player import Player
from maze import Maze
class Movement(Player):
    def __init__(self, maze, player):
        self.maze = maze
        self.player = player
        self.center_tiles = self.maze.get_center_tiles()
    def move_forward(self, distance=Player.stepVal):
        

mHeight = Maze.SCREEN_HEIGHT #height of maze
mWidth = Maze.SCREEN_WIDTH #width of maze

dV = 512 # default value for floor tile
hasWallVal = 'x' #value impassible tile/wall tile
noWallVal = ' ' #value of passable tile/no wall
outerWallunseen = 'z'
#TODO: IMPLEMENT CLASSES 
Matrix = []
Visited = [[False for _ in range(2*mWidth+1)] for _ in range(2*mHeight+1)]



#TODO MAKE CENTER DEPENDANT ON MAZE ARRAY
centerTiles = [(15,15), (15,17), (17, 15), (17, 17), (7,7), (7,8), (8,7),(8,8)]

def resetMatrix(Matrix, type='start'):
    for i in range(1, mHeight*2+1, 2):
        for f in range(1, mWidth*2+1, 2):
            Matrix[i][f] = dV
    if type == 'start':
        Matrix[centerTiles[0][0]][centerTiles[0][1]] = 0
        Matrix[centerTiles[1][0]][centerTiles[1][1]] = 0
        Matrix[centerTiles[2][0]][centerTiles[2][1]] = 0
        Matrix[centerTiles[3][0]][centerTiles[3][1]] = 0
    else:
        Matrix[31][1] = 0
        

    return Matrix

def floodFill(image, goal):
    queue = deque(goal) 

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    #               up      right   down     left

    while queue:
        r,c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + 2*dr, c + 2*dc 
            wr, wc = r + dr, c + dc 
            if 0 <= nr <= 2*mWidth and 0 <= nc <= 2*mHeight and image[nr][nc] > image[r][c]+1:
                if image[wr][wc] == noWallVal:
                    image[nr][nc] = image[r][c] + 1
                    queue.append((nr, nc))
                    API.setText(int((nc-1)/2), 15-int((nr-1)/2), image[nr][nc]) 
    return image

def main():
    global Matrix
    start_r, start_c = 31, 1
    current_r, current_c = start_r, start_c
    currentPos = Matrix[current_r][current_c]
    directions1 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    directions2 = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    orientation = 0
    API.setText(centerTiles[4][0], centerTiles[4][1], 0)
    API.setText(centerTiles[5][0], centerTiles[5][1], 0)
    API.setText(centerTiles[6][0], centerTiles[6][1], 0)
    API.setText(centerTiles[7][0], centerTiles[7][1], 0)
    steps = 0
    directionNESW = ('n', 'e', 's', 'w')
    centerGoal = [(15, 15), (17, 17), (17, 15), (15, 17)]
    
    while currentPos > 0:
        wallFound = False
        Visited[current_r][current_c] = True 
    
        lowest = 4028
        next = []
        """neighbours = [
            directions1[orientation],
            directions1[(1+orientation)%4],
            directions1[(2+orientation)%4],
            directions1[(3+orientation)%4]
        ]""" #TODO figure out why this doesnt work when declared outside loop
        neighbours = [
            orientation,
            (1+orientation)%4,
            (2+orientation)%4,
            (3+orientation)%4
        ]

        #TODO: create binary representation of the maze with the first digit
        # 0/1 representing wether it has been visited and the last 4 representing
        #weither there is a wall in that direction (NESW) with 0 or 1


        oR, oC = directions1[neighbours[0]]
        o2R, o2C = 2*oR, 2*oC
        if API.wallFront():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[orientation])
                Matrix[current_r+oR][current_c+oC] = hasWallVal      
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32:
            next.append(0) #o2R, o2C = directions2[dirOffset+orientation]



        oR, oC = directions1[neighbours[1]]
        o2R, o2C = 2*oR, 2*oC
        if API.wallRight():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal: # alt == noWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(1+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal       
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_c < 31:
            next.append(1) #o2R, o2C = directions2[dirOffset+orientation]



        oR, oC = directions1[neighbours[2]]
        o2R, o2C = 2*oR, 2*oC
        if API.wallBack():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(2+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_r < 31:
            next.append(2) #o2R, o2C = directions2[(dirOffset+orientation)%4]



        oR, oC = directions1[neighbours[3]]
        o2R, o2C = 2*oR, 2*oC
        if API.wallLeft():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(3+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_c > 1:
            next.append(3) #o2R, o2C = directions2[dirOffset+orientation]
        

        if wallFound == True:
            steps+=1
            Matrix = floodFill(resetMatrix(Matrix), centerGoal)
        """          5      4      3      2      1
        0123 score = 391.6, 620.4, 496.1, 107.9, 369.6
        0132 score = 871.2, 620.4, 324.5, 107.9, 369.6
        0312 score = 884.4, 673.2, 324.5, 107.9, 369.6
        0321 score = 884.4, 653.4, 324.5, 107.9, 369.6
        0213 score = 391.6, 620.4, 496.1, 107.9, 369.6
        0231 score = 391.6, 653.4, 496.1, 107.9, 369.6
        2310 score = 455.4, 270.6, 337.7, 103.5, 250.8
        3210 score = 882.2, 270.6, 337.7, 103.5, 352
        3102 score = 882.2, 246.4, 337.7, 103.5, 352
        1302 score = 882.2, 246.4, 337.7, 103.5, 352
        
        """

        #TODO add weighted direcetions for priority chosing

        if 0 in next: 
            er, ec = directions2[neighbours[0]]
            x = Matrix[current_r+er][current_c+ec]
            if x < lowest: 
                dirOffset = 0
                lowest = x
        
        if 1 in next: 
            er, ec = directions2[neighbours[1]]
            x = Matrix[current_r+er][current_c+ec]
            if x < lowest:
                dirOffset = 1
                lowest = x

        if 2 in next: 
            er, ec = directions2[neighbours[2]]
            x = Matrix[current_r+er][current_c+ec]
            if x < lowest:
                dirOffset = 2
                lowest = x

        if 3 in next:
            er, ec = directions2[neighbours[3]]
            x = Matrix[current_r+er][current_c+ec]
            if x < lowest:
                dirOffset = 3
                lowest = x 



        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        
        tOR = (orientation+dirOffset)%4
        er, ec = directions2[tOR]
        
        if dirOffset == 1:
            API.turnRight90()
        elif dirOffset == 2:
            API.turnRight90()
            API.turnRight90()
        elif dirOffset == 3:
            API.turnLeft90()
        orientation = tOR
    

        API.moveForward()
        current_r += er
        current_c += ec
        currentPos = Matrix[current_r][current_c]

if __name__ == "__main__":
    main()
