from turtle import update
import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH
from math import sqrt

from util import Point, Fringe

def parse_8n_grid(filename):
    with open(filename) as f:
        lines = f.read().split("\n")
        start_line = lines[0].split(" ")
        start_vertex = Point(int(start_line[0]), int(start_line[1]))
        end_line = lines[1].split(" ")
        end_vertex = Point(int(end_line[0]), int(end_line[1]))
        dim_line = lines[2].split(" ")
        grid_dimensions = (int(dim_line[0]), int(dim_line[1]))
        grid = np.zeros(grid_dimensions)
        for line in lines[3:]:
            vals = line.split(" ")
            x = int(vals[0])
            y = int(vals[1])
            free = int(vals[2])
            grid[y-1,x-1] = free
        return (grid, start_vertex, end_vertex)

def on_edge(grid, cell):
    return cell.x < 0 or cell.x >= grid.shape[0] or cell.y < 0 or cell.y >= grid.shape[1]

def get_vertex_edges(cell_grid):
    padded_grid = np.pad(cell_grid, 1, 'constant', constant_values=1)
    graph = np.zeros((cell_grid.shape[0]+1, cell_grid.shape[1]+1))
    num_vertices = graph.shape[0]*graph.shape[1]
    adjacency_grid = np.zeros((num_vertices, num_vertices))
    adjacency_dict = {}
    adjacency_lookup = {}
    count = 0
    for x in range(graph.shape[0]):
        for y in range(graph.shape[1]):
            vertex_hash = hash((x, y))
            if vertex_hash not in adjacency_dict:
                adjacency_dict[vertex_hash] = count
                adjacency_lookup[count] = Point(x, y)
                count = count+1
    adjacent_vertices = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]
    diag_vertices = [Point(-1, -1), Point(-1, 1), Point(1, 1), Point(1, -1)]
    adjacent_cells = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0), Point(0, 0)]
    for x in range(graph.shape[0]):
        for y in range(graph.shape[1]):
            vertex_hash = hash((x, y))
            for c_i in range(len(adjacent_cells)-1):
                base_cell = Point(x, y)
                c1 = base_cell+adjacent_cells[c_i]
                c2 = base_cell+adjacent_cells[c_i+1]
                a1 = adjacency_dict[hash(base_cell)]
                if not on_edge(padded_grid, c1) and not on_edge(padded_grid, c2):
                    adjacent = 1
                    if padded_grid[c1.y, c1.x] == 1 and padded_grid[c2.y, c2.x] == 1:
                        adjacent = 0
                    if not on_edge(graph, (base_cell + adjacent_vertices[c_i])):
                        a2 = adjacency_dict[hash(base_cell + adjacent_vertices[c_i])]
                        adjacency_grid[a1, a2] = adjacent
                        adjacency_grid[a2, a1] = adjacent
                
                if padded_grid[c1.y, c1.x] == 0 and not on_edge(graph, (base_cell + diag_vertices[c_i])):
                    a2 = adjacency_dict[hash(base_cell + diag_vertices[c_i])]
                    adjacency_grid[a1, a2] = 1
                    adjacency_grid[a2, a1] = 1
    return (graph, adjacency_dict, adjacency_grid, adjacency_lookup)

def display_grid(cell_grid, path):
    EMPTY_CELL = "#ffffff"
    FILLED_CELL = "#777777"
    DIMENSIONS = (500, 500)
    frame = Tk()
    frame.geometry(f'{DIMENSIONS[0]}x{DIMENSIONS[1]}+550+550')
    canvas = Canvas(frame, width=DIMENSIONS[0], height=DIMENSIONS[1], background='white')
    canvas.pack()
    rect_dim = (DIMENSIONS[0]//cell_grid.shape[0], DIMENSIONS[1]//cell_grid.shape[1])
    graph, adjacency_dict, adjacency_list, adjacency_lookup = get_vertex_edges(cell_grid)
    for x in range(cell_grid.shape[0]):
        for y in range(cell_grid.shape[1]):
            color = EMPTY_CELL if cell_grid[y, x] == 0 else FILLED_CELL
            canvas.create_rectangle(
                x*rect_dim[0], y*rect_dim[1], (x+1)*rect_dim[0], (y+1)*rect_dim[1],
                outline = "#000000",
                fill = color
            )
    # for x1 in range(graph.shape[0]):
    #     for y1 in range(graph.shape[1]):
    #         for x2 in range(graph.shape[0]):
    #             for y2 in range(graph.shape[1]):
    #                 p1 = Point(x1, y1)
    #                 p2 = Point(x2, y2)
    #                 if p1 != p2 and adjacency_list[adjacency_dict[hash(p1)], adjacency_dict[hash(p2)]] == 1:
    #                     canvas.create_line(
    #                         p1.x*rect_dim[0], p1.y*rect_dim[1], p2.x*rect_dim[0], p2.y*rect_dim[1],
    #                         fill='red',
    #                         width=5
    #                     )
    for i in range(len(path)-1):
        p1 = path[i]
        p2 = path[i+1]
        canvas.create_line(
            p1.x*rect_dim[0], p1.y*rect_dim[1], p2.x*rect_dim[0], p2.y*rect_dim[1],
            fill='red',
            width=5
        )
    frame.mainloop()
    return    

def h(v, g):
    return sqrt(2)*min(abs(v.x-g.x), abs(v.y-g.y)) + max(abs(v.x-g.x), abs(v.y-g.y)) - min(abs(v.x-g.x), (v.y-g.y))

def update_vertex(parent, child, cost, parent_map, fringe, goal):
    if cost[parent.y, parent.x] + parent.dist(child) < cost[child.y, child.x]:
        cost[child.y, child.x] = cost[parent.y, parent.x] + parent.dist(child) 
        parent_map[child.y, child.x] = (parent.x, parent.y)
        if child in fringe:
            fringe.remove(child)
        fringe.insert(child, cost[child.y, child.x] + h(child, goal))

def a_star(cell_grid, start, goal):
    graph, adjacency_dict, adjacency_grid, adjacency_lookup = get_vertex_edges(cell_grid)
    cost = np.zeros(graph.shape)
    cost[start.y, start.x] = 0
    fringe = Fringe()
    fringe.insert(start, cost[start.y, start.x] + h(start, goal))
    parent = np.zeros((graph.shape[0], graph.shape[1], 2))
    parent[start.y, start.x] = (start.x, start.y)
    closed = []
    while not fringe.is_empty():
        v = fringe.pop()
        if v[0] == goal:
            return parent
        closed.append(v[0])
        neighbors = []
        adjacent = adjacency_grid[adjacency_dict[hash(v[0])], :]
        for a_i in range(len(adjacent)):
            if adjacent[a_i] == 1:
                neighbors.append(adjacency_lookup[a_i])
        for n in neighbors:
            if n not in closed:
                if n not in fringe:
                    cost[n.y, n.x] = float("inf")
                    parent[n.y, n.x] = None
                update_vertex(v[0], n, cost, parent, fringe, goal)
    return "No Path"



f_name = "grid_1"
if __name__ == "__main__":
    grid, start, goal = parse_8n_grid(f_name)    
    parent = a_star(grid, start, goal)
    path = []
    curr_v = goal
    while curr_v != start:
        print(curr_v, start)
        path.insert(0, curr_v)
        parent_v = parent[curr_v.y, curr_v.x, :]
        curr_v = Point(int(parent_v[0]), int(parent_v[1]))
    path.insert(0, curr_v)
    display_grid(grid, path)

