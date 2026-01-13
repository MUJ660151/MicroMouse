from collections import deque
import API
import sys
mHeight = API.mazeHeight() #height of maze
mWidth = API.mazeWidth() #width of maze

dV = 512 # default value for floor tile
hasWallVal = 'x' #value impassible tile/wall tile
noWallVal = 'o' #value of passable or unknown tile/no known wall
Matrix = [[dV for x in range(mWidth)] for y in range(mHeight)]
#TODO make center scale to different maze dimensions
owRow = [hasWallVal for x in range(mWidth*2+1)]
wMatrix = [owRow] #walled matrix, each floor tile is surrounded on all sides


#TODO: change following forloop so that it creates the matrix using 
#even/odd and detecting edges instead of iterating over another 2dlist
for r, row in enumerate(Matrix):
    sublist = [hasWallVal]
    iwRow = [hasWallVal]
    for i, item in enumerate(row):
        sublist.append(item)
        if i < 15:
            sublist.append(noWallVal)
        else:
            sublist.append(hasWallVal)
    wMatrix.append(sublist)
    if r <15:
        wMatrix.append(iwRow)
    else:
        wMatrix.append(owRow)

for i in range(mHeight*2+1):
    sublist = []
    if i % 2 != 0:
        for c in range(mWidth*2+1):
            pass


centerTiles = [(15,15), (17,17), (15, 17), (17, 15)]

for r, c in centerTiles:
    wMatrix[r][c] = 0
    API.setText(int((r-1)/2), int((c-1)/2), 0)



def resetMatrix(wMatrix):
    for i in range(1, mHeight*2+1, 2):
        for f in range(1, mWidth*2+1, 2):
            wMatrix[i][f] = dV
    for r,c in centerTiles:
        wMatrix[r][c] = 0
    return wMatrix
            
    #resets value of non wall tiles by itterating over odd indexes

def floodFill(image):
    #TODO make queue work with any dimension maze
    queue = deque([(15, 15), (17, 17), (17, 15), (15, 17)]) #note the order for these matters 
    #TODO find best order for queue

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    #               up      right   down     left
    # marker, x, y
    #TODO: make tile values change based on discovered walls
    #TODO: fix all lower right quadrant values being 1 too high
    while queue:
        r,c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + 2*dr, c + 2*dc #floor tile coords in direction
            wr, wc = r + dr, c + dc #wall tile coords in direction
            #if 0 <= nr < 2*mWidth+1 and 0 <= nc < 2*mHeight+1 and image[nr][nc] == 512: #leaves lover left quadraant super high
            if 0 <= nr <= 2*mWidth and 0 <= nc <= 2*mHeight and image[nr][nc] > image[r][c]+1:
                if image[wr][wc] == noWallVal:
                    image[nr][nc] = image[r][c] + 1
                    queue.append((nr, nc))
                    API.setText(int((nr)/2), int((nc)/2), image[nr][nc])
    return image

def main():
    global wMatrix
    start_r, start_c = 31, 1
    current_r, current_c = start_r, start_c
    currentPos = wMatrix[current_r][current_c]
    orientation = 0
    while currentPos > 0:
        wMatrix = floodFill(resetMatrix(wMatrix))
        for row in wMatrix:
            print(*row)
        '''
        for row in result: #to edit
            print(*row)
        '''
        dr, dc = 0, 0
        lowest = 4028

        #TODO: makesure that lowest isnt trying to count tiles beyond edges
        if API.wallFront():
            wMatrix[current_r-1][current_c] = hasWallVal
            #TODO: STOP THSI FROM HAPPENING IN EVERY ROW
        else:
            lowest = wMatrix[current_r-2][current_c]
            dc, dr = 0, -2
            tdir = 0 

        if API.wallRight():
            wMatrix[current_r][current_c+1] = hasWallVal
        elif lowest > wMatrix[current_r][current_c+2]:
            lowest = wMatrix[current_r][current_c+2]
            dc, dr = 2, 0
            tdir = 1
        
        if API.wallBack():
            wMatrix[current_r+1][current_c] = hasWallVal
        elif lowest > wMatrix[current_r+2][current_c]:
            lowest = wMatrix[current_r+2][current_c]
            dc, dr = 0, 2
            tdir = 2
        
        if API.wallLeft():
            wMatrix[current_r][current_c-1] = hasWallVal
        elif lowest > wMatrix[current_r][current_c-2]:
            lowest = wMatrix[current_r][current_c-2]
            dc, dr = -2, 0
            tdir = 3

        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        while orientation != tdir: #TODO: add fastest path algorith/ability to turn left or right depending on whats closer to target
            API.turnRight90()
            if orientation < 3:
                orientation += 1
            else:
                orientation = 0
            print(orientation, tdir)
        API.moveForward()
        current_r += dr
        current_c += dc
        currentPos = wMatrix[current_r][current_c]

if __name__ == "__main__":
    main()
