"""Simple Vehicles Routing Problem."""
import numpy as np
import timeit

import christofides_tsp
from utils import *
from Sets import Sets
from Set import Set
home = Waypoint(0, 0, 50.0)

TIME_LIMIT = 1
num_vehicles = 1
samples = 20
np.set_printoptions( threshold=1000, linewidth=1000)

def get_cost(distance_matrix, path):
    cost = 0
    for i in range(1, len(path), 1):
        cost += distance_matrix[i-1][i]
    return cost


if __name__ == '__main__':
    start_time = timeit.default_timer()
    sorted = build_graph(samples)
    print(sorted)
    # graph = np.array(sorted)
    p = []
    edges = []
    path = Edge(0, 0, 0)
    my_set = None

    while True:
        for edge in sorted:
            print(edge.start, edge.end)
            start = edge.start
            end = edge.end
            if my_set is None:
                my_set = Set(start, end)
            else:
                my_set.add(start, end)

        for node in my_set.nodes:
            print(node)

        print(len(my_set.nodes))
        # for node in my_set.nodes:
        #     print(node in my_set.nodes)
        #     # print(node)
        if len(my_set.nodes) is samples:
            break

    ans = ''
    for node in my_set.nodes:
        print(node)

    for node in my_set.nodes:
        ans += str(node.id) + ','
    print(ans)






    # print(graph)
    # path = christofides_tsp.christofides_tsp(graph)
    # cost = get_cost(distance_matrix, path)
    # print('christofides path', path, 'cost', cost)
    #
    # plot_results([path], waypoints, home, num_vehicles, 'christofides.png')
    # path = [0, 4, 2, 1, 5, 7, 6, 18, 14, 10, 11, 8, 9, 13, 15, 17, 19, 16, 12, 3]
    # plot_results([path], waypoints, home, num_vehicles, 'pso.png')
    # # christofides_tsp(graph)
    stop_time = timeit.default_timer()
    print('time elapsed', stop_time - start_time)
