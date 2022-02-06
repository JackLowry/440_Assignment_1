import random
import numpy as np
from util import Point
from parse import get_vertex_edges
def valid_path(grid, start, goal):
    graph, adjacency_dict, adjacency_grid, adjacency_lookup = get_vertex_edges(grid)
    closed = []
    closed.append(start)
    neighbors = []
    
    adjacent = adjacency_grid[adjacency_dict[hash(start)], :]
    for a_i in range(len(adjacent)):
        if adjacent[a_i] == 1:
            neighbors.append(adjacency_lookup[a_i])
    while len(neighbors) > 0:
        n = neighbors.pop(0)
        if n == goal:
            return True
        adjacent = adjacency_grid[adjacency_dict[hash(n)], :]
        for a_i in range(len(adjacent)):
            if adjacent[a_i] == 1:
                neighbors.append(adjacency_lookup[a_i])
    return False
    

def generate_grids(n, w, h):
    with open("grids/count.txt") as count_f:
        count = int(count_f.read())
    for i in range(count, count+n):
        valid = False
        while not valid:
            grid = np.zeros((w, h))
            for x in range(len(grid)):
                for y in range(len(grid[x])):
                    grid[x, y] = 0 if random.randint(0, 9) < 9 else 1
            start = Point(random.randint(0, w), random.randint(0, h))
            goal = Point(random.randint(0, w), random.randint(0, h))
            print("hi", start, goal)
            while goal == start:
                goal = Point(random.randint(0, w), random.randint(0, h))
            valid = valid_path(grid, start, goal)
        with open("grids/grid_" + str(count), "w") as f:
            f.write(f"{start.x+1} {start.x+1}\n")
            f.write(f"{goal.x+1} {goal.x+1}\n")
            f.write(f"{start.x} {start.x}\n")
            f.write(f"{w} {h}")
            for x in range(grid.shape[0]):
                for y in range(grid.shape[1]):
                    f.write(f"\n{x+1} {y+1} {grid[y, x]}")

if __name__ == "__main__":
    generate_grids(50, 100, 50)

        