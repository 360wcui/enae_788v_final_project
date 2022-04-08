"""Simple Vehicles Routing Problem."""
import math
import numpy as np
import timeit

import held_karp
from utils import *

TIME_LIMIT  = 1
num_vehicles = 1
samples = 20
home = Waypoint(0, 0, 50)

# iterate through all the starting and end points to find the best route that traverses all the nodes.
if __name__ == '__main__':
    start = timeit.default_timer()
    distance_matrix, waypoints = build_distance_matrix(samples, home)
    cost, path = held_karp.held_karp(distance_matrix)
    print('held karp path', path, 'cost', cost)
    plot_results([path], waypoints, None, num_vehicles, 'held_karp.png')
    stop = timeit.default_timer()

    print('time elapsed', stop - start)
