from collections import deque
import API
import sys
mHeight = API.mazeHeight() #height of maze
mWidth = API.mazeWidth() #width of maze

dV = 512 # default value for floor tile
hasWallVal = 'x' #value impassible tile/wall tile
noWallVal = 'o' #value of passable tile/no wall
outerWallunseen = 'z'

Matrix = []

for i in range(mHeight*2+1): #creates each row
    sublist = []
    for e in range(mWidth*2+1):
        if 0 < i < 2*mWidth and 0 < e < 2*mWidth:
            if i % 2 != 0:
                if e % 2 != 0: #if  an odd column
                    sublist.append(dV)
                else: #elif 0 < e < 2*mWidth:
                    sublist.append(noWallVal)
                #else:
                    #sublist.append(hasWallVal)
            else:
                if e % 2 != 0:
                    sublist.append(noWallVal)
                else:
                    sublist.append(hasWallVal)
        else:
            sublist.append(outerWallunseen)
    Matrix.append(sublist)


#TODO make center scale to different maze dimensions
centerTiles = [(15,15), (15,17), (17, 15), (17, 17), (7,7), (7,8), (8,7),(8,8)]

def resetMatrix(Matrix):
    for i in range(1, mHeight*2+1, 2):
        for f in range(1, mWidth*2+1, 2):
            Matrix[i][f] = dV
    Matrix[centerTiles[0][0]][centerTiles[0][1]] = 0
    Matrix[centerTiles[1][0]][centerTiles[1][1]] = 0
    Matrix[centerTiles[2][0]][centerTiles[2][1]] = 0
    Matrix[centerTiles[3][0]][centerTiles[3][1]] = 0
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

'''
def withinLimits(x, y):
    if 0 <= x < 32 and 0 <= y < 32:
        return True
    return False'''

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

    while currentPos > 0:
        wallFound = False

        lowest = 4028
        #TODO fix mouse sometimes needing to backtrack to update
        #this is because the values of the tiles around it dont update
        #until after it decides which is lowest

        oR, oC = directions1[orientation]
        o2R, o2C = 2*oR, 2*oC
        if API.wallFront():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[orientation])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32:
            lowest = Matrix[current_r+o2R][current_c+o2C]
            dirOffset = 0


        oR, oC = directions1[(1+orientation)%4]
        o2R, o2C = 2*oR, 2*oC
        if API.wallRight():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal: # alt == noWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(1+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_c < 31:
            if lowest > Matrix[current_r+o2R][current_c+o2C]:
                lowest = Matrix[current_r+o2R][current_c+o2C]
                dirOffset = 1
            #elif lowest == Matrix[current_r+o2R][current_c+o2C]:

        oR, oC = directions1[(2+orientation)%4]
        o2R, o2C = 2*oR, 2*oC
        if API.wallBack():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(2+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_r < 31:
            if lowest > Matrix[current_r+o2R][current_c+o2C]:
                lowest = Matrix[current_r+o2R][current_c+o2C]
                dirOffset = 2

        oR, oC = directions1[(3+orientation)%4]
        o2R, o2C = 2*oR, 2*oC
        if API.wallLeft():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(3+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_c > 1:
            if lowest > Matrix[current_r+o2R][current_c+o2C]:
                lowest = Matrix[current_r+o2R][current_c+o2C]
                dirOffset = 3
        

        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        
        if wallFound:
            steps+=1
            Matrix = floodFill(resetMatrix(Matrix))
            for row in Matrix:
                for item in row:
                    print(f"{str(item):^2}", end="")
                print()
        tOR = (orientation+dirOffset)%4
        er, ec = directions2[tOR]

        turns = (tOR - orientation) % 4
        
        if turns == 1:
            API.turnRight90()
        elif turns == 2:
            API.turnRight90()
            API.turnRight90()
        elif turns == 3:
            API.turnLeft90()
        orientation = tOR
    

        API.moveForward()
        current_r += er
        current_c += ec
        currentPos = Matrix[current_r][current_c]
    print(steps)

if __name__ == "__main__":
    main()

"""
    f   r   b   l
0   0   1   2   3
1   1   2   3   0
2   2   3   0   1
3   3   0   1   2
"""