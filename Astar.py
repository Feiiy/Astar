import heapq

class Node:
    def __init__(self, x, y, obstacle=False):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.g = float('inf')
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def get_neighbors(grid, node):
    neighbors = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        x = node.x + dx
        y = node.y + dy
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and not grid[x][y].obstacle:
            neighbors.append(grid[x][y])
    return neighbors

def a_star(grid, start, goal):
    open_list = []
    heapq.heappush(open_list, start)
    start.g = 0

    while open_list:
        current_node = heapq.heappop(open_list)
        if current_node == goal:
            return get_path(current_node)

        neighbors = get_neighbors(grid, current_node)
        for neighbor in neighbors:
            new_g = current_node.g + 1
            if new_g < neighbor.g:
                neighbor.g = new_g
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)
                else:
                    # 如果邻居节点已经在开放列表中，更新其代价和父节点 ***
                    index = open_list.index(neighbor)
                    open_list[index] = neighbor
                    heapq.heapify(open_list)

    return None

def get_path(node):
    path = []
    current = node
    while current is not None:
        path.append((current.x, current.y))
        current = current.parent
    return path[::-1]

def generate_grid(n, obstacle_prob):
    grid = [[Node(x, y) for y in range(n)] for x in range(n)]
    for row in grid:
        for node in row:
            if node.x == 0 and node.y == 0:
                start = node
            elif node.x == n - 1 and node.y == n - 1:
                goal = node
            else:
                if random.random() < obstacle_prob:
                    node.obstacle = True
    return grid, start, goal

def print_grid(grid, path=None):
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if path and (i, j) in path:
                print('P', end=' ')
            elif grid[i][j].obstacle:
                print('#', end=' ')
            else:
                print('.', end=' ')
        print()

import random

n = 5
obstacle_prob = 0.2

grid, start, goal = generate_grid(n, obstacle_prob)
path = a_star(grid, start, goal)

print("起点坐标：(0, 0)")
print("终点坐标：({}, {})".format(n - 1, n - 1))
print("\n网格：")
print_grid(grid, path)

if path:
    print("\n最优路径：")
    print(path)
else:
    print("\n无法找到路径！")