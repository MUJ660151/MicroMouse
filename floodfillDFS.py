def floodFill(image, x, y, targetColor, color):
    if (x < 0 or x >= len(image) or
        y < 0 or y >= len(image[0]) or
        image[x][y] != targetColor):
        return
    image[x][y] = color

    floodFill(image, x + 1, y, targetColor, color)
    floodFill(image, x - 1, y, targetColor, color)
    floodFill(image, x, y + 1, targetColor, color)
    floodFill(image, x, y - 1, targetColor, color) 

def Main(image, sr, sc, color):

    if image[sr][sc] == color:
        return image
    
    targetColor = image[sr][sc]
    floodFill(image, sr, sc, targetColor, color)

    return image

image = [
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 1, 1]
    ]
sr, sc = 1, 2
color = 2
result = Main(image, sr, sc, color)
for row in result:
    print(*row)