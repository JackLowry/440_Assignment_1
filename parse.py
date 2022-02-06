import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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
        return grid

def on_edge(grid, cell):
    return cell.x == 0 or cell.x == grid.shape[0]-1 or cell.y == 0 or cell.y == grid.shape[1]-1

def get_vertex_edges(cell_grid):
    padded_grid = np.pad(cell_grid, 1, 'constant', constant_values=1)
    graph = np.zeros((cell_grid.shape[0]+1, cell_grid.shape[1]+1))
    num_vertices = graph.shape[0]*graph.shape[1]
    adjacency_grid = np.zeros((num_vertices, num_vertices))
    adjacency_dict = {}
    count = 0
    for x in range(graph.shape[0]):
        for y in range(graph.shape[1]):
            vertex_hash = hash((x, y))
            if vertex_hash not in adjacency_dict:
                adjacency_dict[vertex_hash] = count
                count = count+1
    adjacent_vertices = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]
    adjacent_cells = [Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0), Point(0, 0)]
    for x in range(graph.shape[0]):
        for y in range(graph.shape[1]):
            vertex_hash = hash((x, y))
            for c_i in range(len(adjacent_cells)-1):
                base_cell = Point(x, y)
                c1 = base_cell+adjacent_cells[c_i]
                c2 = base_cell+adjacent_cells[c_i+1]
                adjacent = 1
                if cell_grid[c1.y, c1.x] == 1 and cell_grid[c2.y, c2.x] == 1 and not on_edge(padded_grid, c1) and not on_edge(padded_grid, c2):
                    adjacent = 0
                a1 = adjacency_dict[hash(base_cell)]
                a2 = adjacency_dict[hash(base_cell + adjacent_vertices[c_i])]
                adjacency_grid[a1, a2] = adjacent
                adjacency_grid[a2, a1] = adjacent
    return (graph, adjacency_dict, adjacency_grid)

def display_grid(cell_grid):
    EMPTY_CELL = "#ffffff"
    FILLED_CELL = "#777777"
    DIMENSIONS = (500, 500)
    frame = Tk()
    frame.geometry(f'{DIMENSIONS[0]}x{DIMENSIONS[1]}+550+550')
    canvas = Canvas(frame, width=DIMENSIONS[0], height=DIMENSIONS[1], background='white')
    canvas.pack()
    rect_dim = (DIMENSIONS[0]//cell_grid.shape[0], DIMENSIONS[1]//cell_grid.shape[1])
    graph, adjacency_dict, adjacency_list = get_vertex_edges(cell_grid)
    for x in range(cell_grid.shape[0]):
        for y in range(cell_grid.shape[1]):
            print((x*rect_dim[0], y*rect_dim[1], (x+1)*rect_dim[0], (y+1)*rect_dim[1]))
            color = EMPTY_CELL if cell_grid[y, x] == 0 else FILLED_CELL
            canvas.create_rectangle(
                x*rect_dim[0], y*rect_dim[1], (x+1)*rect_dim[0], (y+1)*rect_dim[1],
                outline = "#000000",
                fill = color
            )
    for x1 in range(graph.shape[0]):
        for y1 in range(graph.shape[1]):
            for x2 in range(graph.shape[0]):
                for y2 in range(graph.shape[1]):
                    p1 = Point(x1, y1)
                    p2 = Point(x2, y2)
                    if p1 != p2 and adjacency_list[adjacency_dict[hash(p1)], adjacency_dict[hash(p2)]] == 1:
                        canvas.create_line(
                            p1.x, p1.y, p2.x, p2.y,
                            fill='red',
                            width=5
                        )
                    elif p1 != p2:
                        canvas.create_line(
                            p1.x, p1.y, p2.x, p2.y,
                            fill='blue',
                            width=5
                        )


                    
            

    frame.mainloop()
    return    

f_name = "grid_1"
if __name__ == "__main__":
    grid = parse_8n_grid(f_name)    
    display_grid(grid)

