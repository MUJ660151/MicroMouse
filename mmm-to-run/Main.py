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

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    #               up      right   down     left

    #TODO: make tile values change based on discovered walls
    while queue:
        r,c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + 2*dr, c + 2*dc #floor tile coords in direction
            wr, wc = r + dr, c + dc #wall tile coords in direction

            if 0 <= nr <= 2*mWidth and 0 <= nc <= 2*mHeight and image[nr][nc] > image[r][c]+1:
                if image[wr][wc] == noWallVal:
                    image[nr][nc] = image[r][c] + 1
                    queue.append((nr, nc))
                    API.setText(int((nr)/2), int((nc)/2), image[nr][nc])
    return image

def main():
    global Matrix
    start_r, start_c = 31, 1
    current_r, current_c = start_r, start_c
    currentPos = Matrix[current_r][current_c]
    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
    orientation = 0
    while currentPos > 0:
        Matrix = floodFill(resetMatrix(Matrix))
        for r,c in centerTiles:
            API.setText(int((r-1)/2), int((c-1)/2), 0)
        for row in Matrix:
            for item in row:
                print(f"{str(item):^2}", end="")
            print()

        dr, dc = 0, 0
        lowest = 4028

        #TODO: makesure that lowest isnt trying to count tiles beyond edges
        if API.wallFront():
            print("front")
            Matrix[current_r-1][current_c] = hasWallVal
        elif current_r > 1:
            lowest = Matrix[current_r-2][current_c]
            dc, dr = 0, -2
            tdir = 0 

        if API.wallRight():
            print("right")
            Matrix[current_r][current_c+1] = hasWallVal
        elif current_c < 31:
            if lowest > Matrix[current_r][current_c+2]:
                lowest = Matrix[current_r][current_c+2]
                dc, dr = 2, 0
                tdir = 1
        
        if API.wallBack():
            print("back")
            Matrix[current_r+1][current_c] = hasWallVal
        elif current_r < 31:
            if lowest > Matrix[current_r+2][current_c]:
                lowest = Matrix[current_r+2][current_c]
                dc, dr = 0, 2
                tdir = 2
        
        if API.wallLeft():
            print("left")
            Matrix[current_r][current_c-1] = hasWallVal
        elif current_c > 1:
            if lowest > Matrix[current_r][current_c-2]:
                lowest = Matrix[current_r][current_c-2]
                dc, dr = -2, 0
                tdir = 3
        
        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        while orientation != tdir: #TODO: add fastest path algorith/ability 
            #to turn left or right depending on whats closer to target
            API.turnRight90()
            if orientation < 3:
                orientation += 1
            else:
                orientation = 0

        ec, er = directions[orientation]
        API.moveForward()
        current_r += dr
        current_c += dc
        currentPos = Matrix[current_r][current_c]
        API.clearAllText()

if __name__ == "__main__":
    main()