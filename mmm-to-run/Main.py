from collections import deque
import API
import sys
mHeight = API.mazeHeight() #height of maze
mWidth = API.mazeWidth() #width of maze

dV = 512 # default value for floor tile
hasWallVal = 'x' #value impassible tile/wall tile
noWallVal = 'o' #value of passable or unknown tile/no known wall

Matrix = []

for i in range(mHeight*2+1): #creates each row
    sublist = []
    for e in range(mWidth*2+1):
        if 0 < i < 2*mWidth:
            if i % 2 != 0:
                if e % 2 != 0: #if  an odd column
                    sublist.append(dV)
                elif 0 < e < 2*mWidth:
                    sublist.append(noWallVal)
                else:
                    sublist.append(hasWallVal)
            else:
                if e % 2 != 0:
                    sublist.append(noWallVal)
                else:
                    sublist.append(hasWallVal)
        else:
            sublist.append(hasWallVal)
    Matrix.append(sublist)


#TODO make center scale to different maze dimensions
centerTiles = [(15,15), (17,17), (15, 17), (17, 15)]

def resetMatrix(Matrix):
    for i in range(1, mHeight*2+1, 2):
        for f in range(1, mWidth*2+1, 2):
            Matrix[i][f] = dV
    for r,c in centerTiles:
        Matrix[r][c] = 0
    return Matrix
            
    #resets value of non wall tiles by itterating over odd indexes

def floodFill(image):
    #TODO make queue work with any dimension maze
    queue = deque([(15, 15), (17, 17), (17, 15), (15, 17)]) #note: the order for these matters 
    #TODO find best order for queue
    #Visited = [[False for _ in range(2*mWidth+1)] for _ in range(2*mHeight+1)]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    #               up      right   down     left

    #TODO: make tile values change based on discovered walls
    while queue:
        r,c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + 2*dr, c + 2*dc #floor tile coords in direction
            wr, wc = r + dr, c + dc #wall tile coords in direction
            if 0 <= nr <= 2*mWidth and 0 <= nc <= 2*mHeight and image[nr][nc] > image[r][c]+1:
                if image[wr][wc] == noWallVal:
                    #Visited[nr][nc] = True
                    image[nr][nc] = image[r][c] + 1
                    queue.append((nr, nc))
                    API.setText(int((nc-1)/2), 15-int((nr-1)/2), image[nr][nc])
    return image
def addWall(x, y, direction):

    pass

def withinLimits(x, y):
    if 0 <= x < 32 and 0 <= y < 32:
        return True
    return False

def main():
    global Matrix
    start_r, start_c = 31, 1
    API.setWall(0,0,'w')
    current_r, current_c = start_r, start_c
    currentPos = Matrix[current_r][current_c]
    directions2 = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    directions1 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    orientation = 0
    er, ec = 0, 0

    directionNESW = ['n', 'e', 's', 'w']

    while currentPos > 0:

        Matrix = floodFill(resetMatrix(Matrix))
        for r,c in centerTiles:
            API.setText(int((c-1)/2), 15-int((r-1)/2), 0)
        """for row in Matrix:
            for item in row:
                print(f"{str(item):^2}", end="")
            print()"""

        lowest = 4028


        o2R, o2C = directions2[orientation]
        if API.wallFront():
            oR, oC = directions1[orientation]
            API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[orientation])
            Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif withinLimits(current_r+o2R, current_c+o2C):
            print(Matrix[current_r+o2R][current_c+o2C])
            lowest = Matrix[current_r+o2R][current_c+o2C]
            dirOffset = 0


        o2R, o2C = directions2[(1+orientation)%4]
        if API.wallRight():
            oR, oC = directions1[(1+orientation)%4]
            API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(1+orientation)%4])
            Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif withinLimits(current_r+o2R, current_c+o2C): #current_c < 31:
            if lowest > Matrix[current_r+o2R][current_c+o2C]:
                lowest = Matrix[current_r+o2R][current_c+o2C]
                dirOffset = 1
        

        o2R, o2C = directions2[(2+orientation)%4]
        if API.wallBack():
            oR, oC = directions1[(2+orientation)%4]
            print("back", oR, oC, (2+orientation)%4)
            API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(2+orientation)%4])
            Matrix[current_r+oR][current_c+oC] = hasWallVal
            # +1 
        elif withinLimits(current_r+o2R, current_c+o2C): #current_r < 31:
            print(Matrix[current_r+o2R][current_c+o2C])
            if lowest > Matrix[current_r+o2R][current_c+o2C]:
                lowest = Matrix[current_r+o2R][current_c+o2C]
                dirOffset = 2
        

        o2R, o2C = directions2[(3+orientation)%4]
        if API.wallLeft():
            oR, oC = directions1[(3+orientation)%4]
            print("left", oR, oC, (3+orientation)%4)
            API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(3+orientation)%4])
            Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif withinLimits(current_r+o2R, current_c+o2C): #current_c > 1:
            print(Matrix[current_r+o2R][current_c+o2C])
            if lowest > Matrix[current_r+o2R][current_c+o2C]:
                lowest = Matrix[current_r+o2R][current_c+o2C]
                dirOffset = 3

        #TODO FIX BACKTRACKING
        #TODO ADD ABILITY TO TURN LEFT
        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        #orientation = (orientation+tdir)%4

        tOR = (orientation+dirOffset)%4
        er, ec = directions2[tOR]

        while orientation != tOR:
            API.turnRight90()
            if orientation < 3:
                orientation+= 1
            else:
                orientation = 0
        '''
        for i in range(tdir):
            API.turnRight90()
            '''
        API.moveForward()
        API.clearAllText()
        current_r += er
        current_c += ec
        currentPos = Matrix[current_r][current_c]

if __name__ == "__main__":
    main()

"""
    f   r   b   l
0   0   1   2   3
1   1   2   3   0
2   2   3   0   1
3   3   0   1   2
"""