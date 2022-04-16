import timeit
from utils import *

home = Waypoint(0, 0, 50.0)
TIME_LIMIT  = 1
num_vehicles = 1
samples = 20

if __name__ == '__main__':
    start = timeit.default_timer()
    distance_matrix, waypoints = build_distance_matrix(samples, home)
    graph = np.array(distance_matrix)
    mst = minimal_spanning_tree(graph, 'Prim', starting_node=0)
    # cost = get_cost(distance_matrix, path)
    print('christofides path', mst)

    # plot_results([path], waypoints, home, num_vehicles, 'christofides.png')
    # path = [0, 4, 2, 1, 5, 7, 6, 18, 14, 10, 11, 8, 9, 13, 15, 17, 19, 16, 12, 3]
    # plot_results([path], waypoints, home, num_vehicles, 'pso.png')
    # # christofides_tsp(graph)
    # stop = timeit.default_timer()
    # print('time elapsed', stop - start)