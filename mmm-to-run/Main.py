from collections import deque
import API
import sys

mHeight = 16 #API.mazeHeight() #height of maze
mWidth = 16 #API.mazeWidth() #width of maze

def resetMatrix():
    Matrix = [[512 for x in range(mWidth)] for y in range(mHeight)]
    Matrix[7][7] = 0
    Matrix[7][8] = 0
    Matrix[8][7] = 0
    Matrix[8][8] = 0
    return Matrix
"""
Matrix = resetMatrix()

start_x, start_y = 0,0
current_x, current_y = start_x, start_y
currentPos = Matrix[start_x][start_y]

wallMap = [[[0, 0, 0, 0] for x in range(mWidth)] for y in range(mHeight)] #N, E, S, W 1 for a wall, 0 for open or unknown
"""
def floodFill(image, map):

    queue = deque([(7, 7), (7, 8), (8, 7), (8, 8)])

    directions = [(0, 0, -1), (1, 1, 0), (2, 0, 1), (3, -1, 0)]
    #                  up        right      down       left
    # marker, x, y
    while queue:
        r,c = queue.popleft()
        for i, dr, dc in directions:
            nr, nc = r + dr, c + dc
            #if 0 <= nr < 16 and 0 <= nc < 16 and image[nr][nc] == 512:
            if 0 <= nr < mWidth and 0 <= nc < mHeight and image[nr][nc] > image[r][c]+1: #try without +1
                if map[r][c][i] !=1:
                    image[nr][nc] = image[r][c] + 1
                    queue.append((nr, nc))
    return image

def main():
    Matrix = resetMatrix()
    start_x, start_y = 0,0
    current_x, current_y = start_x, start_y
    currentPos = Matrix[start_x][start_y]
    orientation = 0

    wallMap = [[[0, 0, 0, 0] for x in range(mWidth)] for y in range(mHeight)] #N, E, S, W 1 for a wall, 0 for open or unknown
    while currentPos > 0:

        result = floodFill(Matrix, wallMap)
        for row in result: #to edit
            print(*row)
        dr, dc = 0, 0
        lowest = 1024

        if API.wallFront():
            wallMap[current_x][current_y][0] = 1
            if current_y >0:
                wallMap[current_x][current_y-1][2] = 1
        else:
            lowest = Matrix[current_x][current_y-1]
            dr, dc = 0, -1
            tdir = 0

        if API.wallRight():
            wallMap[current_x][current_y][1] = 1
            if current_x <15:
                wallMap[current_x+1][current_y][3] = 1
        elif lowest > Matrix[current_x+1][current_y]:
            lowest = Matrix[current_x+1][current_y]
            dr, dc = 1, 0
            tdir = 1

        if API.wallBack():
            wallMap[current_x][current_y][2] = 1
            if current_y < 15:
                wallMap[current_x][current_y+1][0] = 1
        elif lowest > Matrix[current_x][current_y+1]:
            lowest = Matrix[current_x][current_y+1]
            dr, dc = 0, 1
            tdir = 2

        if API.wallLeft():
            wallMap[current_x][current_y][3] = 1
            if current_x > 0:
                wallMap[current_x-1][current_y][1] = 1
        elif lowest > Matrix[current_x-1][current_y]:
            lowest = Matrix[current_x-1][current_y]
            dr, dc = -1, 0
            tdir = 3

        #TODO: ADD DIAGONAL PATH FOLLOWING ABILITIES
        while orientation != tdir: #TODO: add fastest path algorith/ability to turn left or right depending on whats closer to target
            API.turnRight90()
            if orientation < 3:
                orientation += 1
            else:
                orientation = 0
        API.moveForward()
        for row in wallMap:
            for group in row:
                print(*group, sep="", end = "|")
            print()
        current_x += dr
        current_y += dc

        Matrix = resetMatrix()

if __name__ == "__main__":
    main()