import API
from collections import deque

m = 16
n = m
center = []
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
'''
directions = {
    'n' : (0, 1),
    'e' : (1, 0),
    's' : (0, -1),
    'w' : (-1, 0)
}
'''
Matrix = [[0000 for x in range(m)] for x in range(n)]
Visited = [False for _ in range(m)]
if m % 2 == 0:
    x = int(m/2)
    y = int(n/2)
    center.append((x, y))
    center.append((x, y-1))
    center.append((x-1, y))
    center.append((x-1, y-1))
else:
    center.append((int(m//2), int(m/2)))
print(center)

def inBounds(x, y):
    return 0 <= x < m and 0 <= y < m

print(inBounds(0, 1))