import time
from parse import h, x_star, update_vertex_a_star, update_vertex_theta_star, parse_8n_grid, display_grid, get_path_len, h2
from util import Point
import sys

grid_num = 50
run_num = 1
fast_fringe_average = 0
length = 0
for i in range(grid_num):
    run_avg = 0
    run_len = 0
    for j in range(run_num):
        grid, start, goal = parse_8n_grid(f"grids/grid_{i}")    
        t0 = time.time()
        closed, cost, parent = x_star(grid, start, goal, update_vertex_theta_star, use_fast_fringe=True, h_fun=h2)
        run_len = length + get_path_len(parent, goal, start)

        closed, cost, parent = x_star(grid, start, goal, update_vertex_theta_star, use_fast_fringe=True)
        t1 = time.time()
        dt = t1-t0
        run_avg = run_avg + dt
    fast_fringe_average = fast_fringe_average + run_avg/run_num
    length = length + run_len/run_num 
    print(str(i))
fast_fringe_average = fast_fringe_average/grid_num
length = length/grid_num
print(f"time: {fast_fringe_average}, length: {length}")
# print("fast_done")
# normal_fringe_average = 0
# for i in range(grid_num):
#     run_avg = 0
#     for j in range(run_num):
#         grid, start, goal = parse_8n_grid(f"grids/grid_{i}")    
#         t0 = time.time()
#         closed, cost, parent = x_star(grid, start, goal, update_vertex_theta_star)
#         t1 = time.time()
#         dt = t1-t0
#         run_avg = run_avg + dt
#     normal_fringe_average = normal_fringe_average + run_avg/run_num
#     print(str(i))
# normal_fringe_average = normal_fringe_average/grid_num

# print(f"normal: {normal_fringe_average}\nfast: {fast_fringe_average}")