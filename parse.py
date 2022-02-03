import numpy as np
from tkinter import Tk, Canvas, Frame, BOTH


def parse_8n_grid(filename):
    with open(filename) as f:
        lines = f.read().split("\n")
        start_line = lines[0].split(" ")
        start_vertex = (int(start_line[0]), int(start_line[1]))
        end_line = lines[1].split(" ")
        end_vertex = (int(end_line[0]), int(end_line[1]))
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

def display_grid(grid):
    EMPTY_CELL = "#ffffff"
    FILLED_CELL = "#777777"
    DIMENSIONS = (500, 500)
    frame = Tk()
    frame.geometry(f'{DIMENSIONS[0]}x{DIMENSIONS[1]}+550+550')
    canvas = Canvas(frame, width=DIMENSIONS[0], height=DIMENSIONS[1], background='white')
    canvas.pack()
    rect_dim = (DIMENSIONS[0]//grid.shape[0], DIMENSIONS[1]//grid.shape[1])
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            print((x*rect_dim[0], y*rect_dim[1], (x+1)*rect_dim[0], (y+1)*rect_dim[1]))
            color = EMPTY_CELL if grid[y, x] == 0 else FILLED_CELL
            canvas.create_rectangle(
                x*rect_dim[0], y*rect_dim[1], (x+1)*rect_dim[0], (y+1)*rect_dim[1],
                outline = "#000000",
                fill = color
            )
    frame.mainloop()
    return

def get_edge_grid(cell_grid):
    padded_grid = np.pad(cell_grid, 1, 'constant', constant_values=1)
    print(padded_grid)
f_name = "grid_1"
if __name__ == "__main__":
    grid = parse_8n_grid(f_name)    
    display_grid(grid)

