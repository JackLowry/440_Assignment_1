from parse import x_star, update_vertex_theta_star, parse_8n_grid, display_grid
from util import Point
import sys
grid, start, goal = parse_8n_grid(sys.argv[1])    
closed, cost, parent = x_star(grid, start, goal, update_vertex_theta_star)
path = []
curr_v = goal
while curr_v != start:
    path.insert(0, curr_v)
    parent_v = parent[curr_v.y, curr_v.x, :]
    curr_v = Point(int(parent_v[0]), int(parent_v[1]))
path.insert(0, curr_v)
display_grid(grid, path, start, goal, cost, parent, closed)