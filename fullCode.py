from collections import deque
import API

mHeight = API.mazeHeight() #height of maze
mWidth = API.mazeWidth() #width of maze

dV = 512 # default value for floor tile
hasWallVal = 'x' #value impassible tile/wall tile
noWallVal = 'o' #value of passable tile/no wall
outerWallunseen = 'z'
#TODO: IMPLEMENT CLASSES 
Matrix = []
Visited = [[False for _ in range(2*mWidth+1)] for _ in range(2*mHeight+1)]

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
            
    #resets value of non wall tiles by itterating over odd indexes

def floodFill(image, goal):
    #TODO make queue work with any dimension maze
    queue = deque(goal) #note: the order for these matters 
    #TODO find best order for queue
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    #               up      right   down     left

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
                    API.setText(int((nc-1)/2), 15-int((nr-1)/2), image[nr][nc]) #TODO: make compatible with different maze sizes
    return image

def addWall(x, y, direction):

    pass

def returnToStart(image, goal, orientation, centerStart, visited):
    currentR, currentC = centerStart[0], centerStart[1]
    print(currentR, currentC)
    #API.setText(int((start[1]-1)/2), 15-int((start[0]-1)/2), 0)
    API.setText(0, 0, 0)
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))
    directionNESW = ('n', 'e', 's', 'w')
    """neighbours = [
            directions[orientation],
            directions[(1+orientation)%4],
            directions[(2+orientation)%4],
            directions[(3+orientation)%4]
        ]"""
    neighbours = [
            orientation,
            (1+orientation)%4,
            (2+orientation)%4,
            (3+orientation)%4
        ]
    image = floodFill(resetMatrix(image, 'return'), [goal]) 
    currentPos = image[currentR][currentC]
    print(currentPos)

    while currentPos > 0:
        """neighbours = [
            orientation,
            (1+orientation)%4,
            (2+orientation)%4,
            (3+orientation)%4
        ]"""
        lowest = 4028
        if visited[currentR][currentC] == False:
            wallFound = False
            #TODO combine these conditions into method 
            oR, oC = directions[neighbours[0]]
            if API.wallFront():
                if image[currentR+oR][currentC+oC] != hasWallVal:
                    wallFound = True
                    API.setWall(int((currentC-1)/2), 15-int((currentR-1)/2), directionNESW[neighbours[0]])
                    image[currentR+oR][currentC+oC] = hasWallVal

            oR, oC = directions[neighbours[1]]
            if API.wallFront():
                if image[currentR+oR][currentC+oC] != hasWallVal:
                    wallFound = True
                    API.setWall(int((currentC-1)/2), 15-int((currentR-1)/2), directionNESW[neighbours[1]])
                    image[currentR+oR][currentC+oC] = hasWallVal      
            
            oR, oC = directions[neighbours[2]]
            if API.wallFront():
                if image[currentR+oR][currentC+oC] != hasWallVal:
                    wallFound = True
                    API.setWall(int((currentC-1)/2), 15-int((currentR-1)/2), directionNESW[neighbours[2]])
                    image[currentR+oR][currentC+oC] = hasWallVal      

            oR, oC = directions[neighbours[3]]
            if API.wallFront():
                if image[currentR+oR][currentC+oC] != hasWallVal:
                    wallFound = True
                    API.setWall(int((currentC-1)/2), 15-int((currentR-1)/2), directionNESW[neighbours[3]])
                    image[currentR+oR][currentC+oC] = hasWallVal      

            if wallFound == True:
                image = floodFill(resetMatrix(image, 'return'), [goal])
                
            visited[currentR][currentC] =True

        tr, tc = directions[neighbours[0]]
        if 0 <= currentR+2*tr < 32 and 0 <= currentC+2*tc < 32:
            if image[currentR+tr][currentC+tc] != hasWallVal:
                if image[currentR+2*tr][currentC+2*tc] < lowest:
                    lowest = image[currentR+2*tr][currentC+2*tc]
                    er, ec = tr, tc
                    tdir = 0

        tr, tc = directions[neighbours[1]]
        if 0 <= currentR+2*tr < 32 and 0 <= currentC+2*tc < 32:
            if image[currentR+tr][currentC+tc] != hasWallVal:
                if image[currentR+2*tr][currentC+2*tc] < lowest:
                    lowest = image[currentR+2*tr][currentC+2*tc]
                    er, ec = tr, tc
                    tdir = 1

        tr, tc = directions[neighbours[2]]
        if 0 <= currentR+2*tr < 32 and 0 <= currentC+2*tc < 32:
            if image[currentR+tr][currentC+tc] != hasWallVal:
                if image[currentR+2*tr][currentC+2*tc] < lowest:
                    lowest = image[currentR+2*tr][currentC+2*tc]
                    er, ec = tr, tc
                    tdir = 2

        tr, tc = directions[neighbours[3]]
        if 0 <= currentR+2*tr < 32 and 0 <= currentC+2*tc < 32:
            if image[currentR+tr][currentC+tc] != hasWallVal:
                if image[currentR+2*tr][currentC+2*tc] < lowest:
                    lowest = image[currentR+2*tr][currentC+2*tc]
                    er, ec = tr, tc
                    tdir = 3
        
        orientation = (orientation+tdir)%4

        currentR += 2*er
        currentC += 2*ec
        currentPos = image[currentR][currentC]



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
    """neighbours = [
            directions2[orientation],
            directions2[(1+orientation)%4],
            directions2[(2+orientation)%4],
            directions2[(3+orientation)%4]
        ]"""
    directionNESW = ('n', 'e', 's', 'w')
    centerGoal = [(15, 15), (17, 17), (17, 15), (15, 17)]

    while currentPos > 0:
        wallFound = False
        Visited[current_r][current_c] = True 
    
        lowest = 4028
        next = []
        neighbours = [
            directions2[orientation],
            directions2[(1+orientation)%4],
            directions2[(2+orientation)%4],
            directions2[(3+orientation)%4]
        ] #TODO see if this works when declared outside the loop

        #TODO fix mouse sometimes needing to backtrack to update
        #this is because the values of the tiles around it dont update
        #until after it decides which is lowest
        #TEMPFIX: reset matrix after each new wall found (done, )
        #LONGFIX: store all potentials coords, then reset, then pick

        #TODO: create binary representation of the maze with the first digit
        # 0/1 representing wether it has been visited and the last 4 representing
        #weither there is a wall in that direction (NESW) with 0 or 1

        #TODO: determine best turn priority when all else is equal
        """if not Visited[current_r][current_c]:
            Visited[current_r][current_c] = True """


        #TODO implement neighbours list
        oR, oC = directions1[orientation]
        o2R, o2C = 2*oR, 2*oC
        if API.wallFront():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[orientation])
                Matrix[current_r+oR][current_c+oC] = hasWallVal      
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32:
            next.append(0) #o2R, o2C = directions2[dirOffset+orientation]



        oR, oC = directions1[(1+orientation)%4]
        o2R, o2C = 2*oR, 2*oC
        if API.wallRight():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal: # alt == noWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(1+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal       
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_c < 31:
            next.append(1) #o2R, o2C = directions2[dirOffset+orientation]



        oR, oC = directions1[(2+orientation)%4]
        o2R, o2C = 2*oR, 2*oC
        if API.wallBack():
            if Matrix[current_r+oR][current_c+oC] != hasWallVal:
                wallFound = True
                API.setWall(int((current_c-1)/2), 15-int((current_r-1)/2), directionNESW[(2+orientation)%4])
                Matrix[current_r+oR][current_c+oC] = hasWallVal
        elif 0 <= current_r+o2R < 32 and 0 <= current_c+o2C < 32: #current_r < 31:
            next.append(2) #o2R, o2C = directions2[(dirOffset+orientation)%4]



        oR, oC = directions1[(3+orientation)%4]
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

        if 0 in next and 0 <= current_r+neighbours[0][0] < 32 and 0 <= current_c+neighbours[0][1] < 32:
            er, ec = neighbours[0]
            lowest = Matrix[current_r+er][current_c+ec]
            dirOffset = 0
        if 1 in next and 0 <= current_r+neighbours[1][0] < 32 and 0 <= current_c+neighbours[1][1] < 32:
            if Matrix[current_r+neighbours[1][0]][current_c+neighbours[1][1]] < lowest:
                er, ec = neighbours[1]
                dirOffset = 1
                lowest = Matrix[current_r+er][current_c+ec]
        if 2 in next and 0 <= current_r+neighbours[2][0] < 32 and 0 <= current_c+neighbours[2][1] < 32:
            if Matrix[current_r+neighbours[2][0]][current_c+neighbours[2][1]] < lowest:
                er, ec = neighbours[2]
                dirOffset = 2
                lowest = Matrix[current_r+er][current_c+ec]
        if 3 in next and 0 <= current_r+neighbours[3][0] < 32 and 0 <= current_c+neighbours[3][1] < 32:
            if Matrix[current_r+neighbours[3][0]][current_c+neighbours[3][1]] < lowest:
                er, ec = neighbours[3]
                dirOffset = 3
                lowest = Matrix[current_r+er][current_c+ec]


        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        
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
    returnToStart(Matrix, (start_r, start_c), orientation, (current_r, current_c), Visited)

if __name__ == "__main__":
    main()

"""
    f   r   b   l
0   0   1   2   3
1   1   2   3   0
2   2   3   0   1
3   3   0   1   2
"""