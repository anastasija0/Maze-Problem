
import numpy as np
import imageio
from PIL import Image, ImageDraw
import queue
import sys
from collections import deque

def read_maze(image_path):
    maze_image = Image.open(image_path).convert("L")  # Convert to grayscale
    binary = maze_image.point(lambda p: p > 128 and 1)  # 1 white 0 black
    return binary
def find_entrance_points(maze):
    width, height = maze.size
    entrance_points = []
    x = 0
    while (x < height):
        if maze.getpixel((0,x)) == 1:
            entrance = []
            while maze.getpixel((0,x)) == 1 and x <= height - 1:
                entrance.append((x, 0))
                x += 1 # Entrance found at the left border
            entrance_points.append(entrance)
        x+=1
    x= 0
    while (x < height):
        if maze.getpixel((width - 1, x)) == 1:  # Entrance found at the right border
            entrance = []
            while maze.getpixel((width - 1, x)) == 1 and x <= height - 1:
                entrance.append((x, width - 1))
                x += 1
            entrance_points.append(entrance)
        x+=1
    y = 0
    while y<=width-1:
        if maze.getpixel((y, 0)) == 1:  # Entrance found at the top border
            entrance = []
            while maze.getpixel((y, 0)) == 1 and y <= width - 1:
                entrance.append((0, y))
                y += 1  # Entrance found at the left border
            entrance_points.append(entrance)
        y+=1
    y = 0
    while y <= width - 1:
        if maze.getpixel((y, 0)) == 1:  # Entrance found at the bottom border
            entrance = []
            while maze.getpixel((y, height - 1)) == 1 and y <= width - 1:
                entrance.append((height - 1, y))
                y += 1  # Entrance found at the left border
            entrance_points.append(entrance)
        y+=1
    return entrance_points

def isValid(row: int, col: int, ROW, COL):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)


import heapq


class Node:
    def __init__(self, x, y, g_cost, h_cost):
        self.x = x
        self.y = y
        self.g_cost = g_cost  # cost from start to current node
        self.h_cost = h_cost  # heuristic cost from current node to end
        self.f_cost = g_cost + h_cost  # total cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost


def heuristic(node, end):
    # Manhattan distance heuristic
    return abs(node.x - end[0]) + abs(node.y - end[1])


def astar(maze, start, end):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    pq = list([(0, Node(start[0], start[1], 0,  abs(start[0] - end[0]) + abs(start[1] - end[1])) )])

    while len(pq)>0:
        _, current_node = heapq.heappop(pq)
        if (current_node.x, current_node.y) == end:
            return current_node.g_cost
        if visited[current_node.x][current_node.y]:
            continue
        visited[current_node.x][current_node.y] = True

        for dx, dy in directions:
            nx, ny = current_node.x + dx, current_node.y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                new_g_cost = current_node.g_cost + 1
                new_h_cost = heuristic(Node(nx, ny,0,0), end)
                new_node = Node(nx, ny, new_g_cost, new_h_cost)
                heapq.heappush(pq, (new_node.f_cost, new_node))
    return -1
def shortest_astar(maze, entrances):
    if len(entrances) == 0 or len(entrances) == 1:
        return -1
    shortest_path = sys.maxsize
    shortest_i = 0
    shortest_j = 0
    for i in range(len(entrances) - 1):
        for j in range(i+1, len(entrances)):
            src = entrances[i][0]
            dst = entrances[j][0]
            path = astar(maze, src, dst)
            if path == -1:
                continue
            if path < shortest_path:
                shortest_path = path
                shortest_i = i
                shortest_j = j

    if shortest_path != sys.maxsize:
        i = shortest_i
        j = shortest_j
        if len(entrances[i]) > 1 or len(entrances[j]) > 1:
            src = entrances[i]
            dst = entrances[j]
            length1 = len(entrances[i])
            length2 = len(entrances[j])
            if (astar(maze, src[0], dst[length2 -1]) < shortest_path and astar(maze, src[0], dst[length2 -1])!= -1):
                shortest_path = astar(maze, src[0], dst[length2 - 1])
            if (astar(maze, src[length1 -1], dst[length2 -1]) < shortest_path and astar(maze, src[length1 -1], dst[length2 -1])!= -1):
                shortest_path = astar(maze, src[length1 - 1], dst[length2 - 1])
            if (astar(maze, src[length1 -1], dst[0]) < shortest_path and astar(maze, src[length1 -1], dst[0]) != -1 ):
                shortest_path = astar(maze, src[length1 -1], dst[0])
        return shortest_path + 1
    else:
        return -1
def astar_teleport(maze, start, end, teleports):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    pq = list([(0, Node(start[0], start[1], 0, 0))])

    while len(pq)>0:
        _, current_node = heapq.heappop(pq)
        if (current_node.x, current_node.y) == end:
            return current_node.g_cost
        if visited[current_node.x][current_node.y]:
            continue
        visited[current_node.x][current_node.y] = True

        for dx, dy in directions:
            nx, ny = current_node.x + dx, current_node.y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                new_g_cost = current_node.g_cost + 1
                new_h_cost = heuristic(Node(nx, ny,0,0), end)
                new_node = Node(nx, ny, new_g_cost, new_h_cost)
                heapq.heappush(pq, (new_node.f_cost, new_node))
            if (nx, ny) in teleports:
                new_g_cost = current_node.g_cost + 0
                new_h_cost = heuristic(Node(nx, ny, 0, 0), end)
                new_node = Node(nx, ny, new_g_cost, new_h_cost)
                heapq.heappush(pq, (new_node.f_cost, new_node))
    return -1
def shortest_astar_teleports(maze, entrances, teleports):
    if len(entrances) == 0 or len(entrances) == 1:
        return -1
    shortest_path = sys.maxsize
    shortest_i = 0
    shortest_j = 0
    for i in range(len(entrances) - 1):
        for j in range(i+1, len(entrances)):
            src = entrances[i][0]
            dst = entrances[j][0]
            path = astar_teleport(maze, src, dst, teleports)
            if path != -1:
                if path < shortest_path:
                    shortest_path = path
                    shortest_i = i
                    shortest_j = j
            else:
                continue

    if shortest_path != sys.maxsize:
        i = shortest_i
        j = shortest_j
        if len(entrances[i]) > 1 or len(entrances[j]) > 1:
            src = entrances[i]
            dst = entrances[j]
            length1 = len(entrances[i])
            length2 = len(entrances[j])
            if (astar_teleport(maze, src[0], dst[length2 - 1], teleports) < shortest_path and astar_teleport(maze, src[0], dst[length2 - 1], teleports) != -1):
                shortest_path = astar_teleport(maze, src[0], dst[length2 - 1],teleports)
            if (astar_teleport(maze, src[length1 - 1], dst[length2 - 1], teleports) < shortest_path and astar_teleport(maze, src[length1 - 1],
                                                                                          dst[length2 - 1], teleports) != -1):
                shortest_path = astar_teleport(maze, src[length1 - 1], dst[length2 - 1], teleports)
            if (astar_teleport(maze, src[length1 - 1], dst[0], teleports) < shortest_path and astar_teleport(maze, src[length1 - 1], dst[0], teleports) != -1):
                shortest_path = astar_teleport(maze, src[length1 - 1], dst[0], teleports)
        return shortest_path + 1
    else:
        return -1


def main():
    image_path = input()
    n = int(input())
    teleports = []
    for i in range(n):
        x, y = map(int, input().split())
        teleports.append((x,y))
    maze = read_maze(image_path)
    mat = np.array(maze)
    entrances= find_entrance_points(maze)
    print(len(entrances))
    shortest = shortest_astar(mat, entrances)
    print(shortest)
    if len(teleports)==0:
        print(shortest)
    else:
        shortest_t = shortest_astar_teleports(mat, entrances, teleports)
        print(shortest_t)


if __name__ == "__main__":
    main()