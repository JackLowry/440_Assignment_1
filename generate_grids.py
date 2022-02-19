import random
import numpy as np
from util import Point
from parse import get_vertex_edges
def valid_path(grid, start, goal):
    graph, adjacency_dict, adjacency_grid, adjacency_lookup = get_vertex_edges(grid)
    closed = [0]*(graph.shape[0]*graph.shape[1])
    closed.append(start)
    neighbors = []
    
    adjacent = adjacency_grid[adjacency_dict[hash(start)], :]
    for a_i in range(len(adjacent)):
        if adjacent[a_i] == 1:
            neighbors.append(adjacency_lookup[a_i])
    while len(neighbors) > 0:
        n = neighbors.pop(0)
        if closed[n.x*n.y+n.x] == 1:
            pass
        if n == goal:
            return True
        adjacent = adjacency_grid[adjacency_dict[hash(n)], :]
        for a_i in range(len(adjacent)):
            if adjacent[a_i] == 1 and closed[n.x*n.y+n.x] == 0:
                neighbors.append(adjacency_lookup[a_i])
        closed[n.x*n.y+n.x] = 1
    return False
    

def generate_grids(n, w, h):
    for i in range(n):
        print("Grid: ", i)
        valid = False
        while not valid:
            grid = np.zeros((h, w))
            for x in range(grid.shape[1]):
                for y in range(grid.shape[0]):
                    grid[y, x] = 0 if random.randint(0, 9) < 8 else 1
            start = Point(random.randint(0, w), random.randint(0, h))
            goal = Point(random.randint(0, w), random.randint(0, h))
            while goal == start:
                goal = Point(random.randint(0, w), random.randint(0, h))
            valid = valid_path(grid, start, goal)
        with open("grids/grid_" + str(i), "w") as f:
            f.write(f"{start.x+1} {start.y+1}\n")
            f.write(f"{goal.x+1} {goal.y+1}\n")
            f.write(f"{w} {h}")
            for x in range(grid.shape[1]):
                for y in range(grid.shape[0]):
                    f.write(f"\n{x+1} {y+1} {int(grid[y, x])}")

if __name__ == "__main__":
    generate_grids(50, 30, 30)

        