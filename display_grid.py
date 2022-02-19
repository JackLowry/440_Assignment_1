import sys
from parse import parse_8n_grid, get_vertex_edges
from tkinter import Tk, Canvas, Frame, BOTH, LAST
def display_grid(cell_grid, start, goal):
    EMPTY_CELL = "#ffffff"
    FILLED_CELL = "#777777"
    DIMENSIONS = (1000, 1000)
    frame = Tk()
    frame.geometry(f'{DIMENSIONS[0]}x{DIMENSIONS[1]}+550+550')
    canvas = Canvas(frame, width=DIMENSIONS[0]+100, height=DIMENSIONS[1]+100, background='white')
    canvas.pack()
    rect_dim = (DIMENSIONS[0]//cell_grid.shape[1], DIMENSIONS[1]//cell_grid.shape[0])
    graph, adjacency_dict, adjacency_list, adjacency_lookup = get_vertex_edges(cell_grid)
    for x in range(cell_grid.shape[1]):
        for y in range(cell_grid.shape[0]):
            color = EMPTY_CELL if cell_grid[y, x] == 0 else FILLED_CELL
            canvas.create_rectangle(
                x*rect_dim[0], y*rect_dim[1], (x+1)*rect_dim[0], (y+1)*rect_dim[1],
                outline = "#000000",
                fill = color
            )

    # for p in closed:
    #     x = p.x
    #     y = p.y
    #     parent_v = parent[y, x]
    #     parent_v = Point(parent_v[0], parent_v[1])
    #     d =  Point(x, y) - parent_v
    #     canvas.create_line( (parent_v.x+d.x)*rect_dim[0], (parent_v.y+d.y)*rect_dim[1], parent_v.x*rect_dim[0], parent_v.y*rect_dim[1], arrow=LAST)  
        #canvas.create_text(x*rect_dim[0], y*rect_dim[1]-10, text=f"{round(cost[y, x], 2)} {round(h(Point(x, y), goal), 2)}", fill="black", font=('Helvetica 8 bold'))
    # for x1 in range(graph.shape[1]):
    #     for y1 in range(graph.shape[0]):
    #         for x2 in range(graph.shape[1]):
    #             for y2 in range(graph.shape[0]):
    #                 p1 = Point(x1, y1)
    #                 p2 = Point(x2, y2)
    #                 if p1 != p2 and adjacency_list[adjacency_dict[hash(p1)], adjacency_dict[hash(p2)]] == 1:
    #                     canvas.create_line(
    #                         p1.x*rect_dim[0], p1.y*rect_dim[1], p2.x*rect_dim[0], p2.y*rect_dim[1],
    #                         fill='red',
    #                         width=1
    #                     )
    # for i in range(len(path)-1):
    #     p1 = path[i]
    #     p2 = path[i+1]
    #     canvas.create_line(
    #         p1.x*rect_dim[0], p1.y*rect_dim[1], p2.x*rect_dim[0], p2.y*rect_dim[1],
    #         fill='red',
    #         width=5
    #     )
    canvas.create_oval(start.x*rect_dim[0]-5, start.y*rect_dim[1]-5, start.x*rect_dim[0]+5, start.y*rect_dim[1]+5, fill='green')
    canvas.create_oval(goal.x*rect_dim[0]-5, goal.y*rect_dim[1]-5, goal.x*rect_dim[0]+5, goal.y*rect_dim[1]+5, fill='blue')
    frame.mainloop()
    return    

if __name__ == "__main__":
    grid, start, goal = parse_8n_grid(sys.argv[1])    
    display_grid(grid, start, goal)
