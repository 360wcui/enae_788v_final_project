"""Simple Vehicles Routing Problem."""
import numpy as np
import timeit

import christofides_tsp
from utils import *

home = Waypoint(0, 0, 50.0)

TIME_LIMIT  = 1
num_vehicles = 1
samples = 20


def get_cost(distance_matrix, path):
    cost = 0
    for i in range(1, len(path), 1):
        cost += distance_matrix[i-1][i]
    return cost


if __name__ == '__main__':
    start = timeit.default_timer()
    distance_matrix, waypoints = build_distance_matrix(samples, home)
    graph = np.array(distance_matrix)
    path = christofides_tsp.christofides_tsp(graph)
    cost = get_cost(distance_matrix, path)
    print('christofides path', path, 'cost', cost)

    plot_results([path], waypoints, home, num_vehicles, 'christofides.png')
    path = [0, 4, 2, 1, 5, 7, 6, 18, 14, 10, 11, 8, 9, 13, 15, 17, 19, 16, 12, 3]
    plot_results([path], waypoints, home, num_vehicles, 'pso.png')
    # christofides_tsp(graph)
    stop = timeit.default_timer()
    print('time elapsed', stop - start)
