from collections import deque;


def floodFill(image, sr, sc, color):

    targetColor = image[sr][sc]

    if targetColor == color:
        return image
        
    queue = deque([(sr, sc)])

    image[sr][sc] = color

    rows = len(image)
    cols = len(image[0])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r,c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == targetColor:
                image[nr][nc] = color
                queue.append((nr, nc))
    return image

image = [
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 1, 1]
    ]
sr, sc = 1, 2
color = 2
result = floodFill(image, sr, sc, color)
for row in result:
    print(*row)