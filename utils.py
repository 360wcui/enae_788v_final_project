import numpy as np

from random import randint
from matplotlib import pyplot as plt
from Waypoint import Waypoint
import math
def minimal_spanning_tree(graph, mode='Prim', starting_node=None):
    """

    Args:
        graph:  weighted adjacency matrix as 2d np.array
        mode: method for calculating minimal spanning tree
        starting_node: node number to start construction of minimal spanning tree (Prim)
    Returns:
        minimal spanning tree as 2d array
    """

    if mode == 'Prim':
        return _minimal_spanning_tree_prim(graph, starting_node)


def _minimal_spanning_tree_prim(graph, starting_node):
    """

    Args:
        graph: weighted adj. matrix as 2d np.array
        starting_node: node number to start construction of minimal spanning tree
    Returns:
        minimal spanning tree as 2d array calculted by Prim
    """

    node_count = len(graph)
    all_nodes = [i for i in range(node_count)]

    if starting_node is None:
        starting_node = randint(0, node_count-1)

    unvisited_nodes = all_nodes
    visited_nodes = [starting_node]
    unvisited_nodes.remove(starting_node)
    mst = np.zeros((node_count, node_count))

    while len(visited_nodes) != node_count:
        selected_subgraph = graph[np.array(visited_nodes)[:, None], np.array(unvisited_nodes)]
        # we mask non-exist edges with -- so it doesn't crash the argmin
        min_edge_index = np.unravel_index(np.ma.masked_equal(selected_subgraph, 0, copy=False).argmin(),
                                          selected_subgraph.shape)
        edge_from = visited_nodes[min_edge_index[0]]
        edge_to = unvisited_nodes[min_edge_index[1]]
        mst[edge_from, edge_to] = graph[edge_from, edge_to]
        mst[edge_to, edge_from] = graph[edge_from, edge_to]
        unvisited_nodes.remove(edge_to)
        visited_nodes.append(edge_to)
    return mst


def route_cost(graph, path):
    cost = 0
    for index in range(len(path) - 1):
        cost = cost + graph[path[index]][path[index + 1]]
    # add last edge to form a cycle.
    cost = cost + graph[path[-1], path[0]]
    return cost


def plot_results(routes, waypoints, home, num_vehicles, filename):
    x = []
    y = []
    plt.figure(1)
    for waypoint in waypoints:
        x.append(waypoint.x)
        y.append(waypoint.y)
    plt.plot(x, y, 'o')
    home_x = waypoints[1].x
    home_y = waypoints[1].y
    for i in range(num_vehicles):
        x = []
        y = []
        for route_index in routes[i]:
            x.append(waypoints[route_index].x)
            y.append(waypoints[route_index].y)
            print(route_index)
        # x.append(home_x)
        # y.append(home_y)
        plt.plot(x, y)
        plt.xlabel('Position (unitless)')
        plt.ylabel('Position (unitless)')
    # plt.plot(home_x, home_y, 'bx', markersize=10)
    # plt.show()
    plt.savefig(filename)
    plt.close(1)


def plot_complete_graph(x, y):
    plt.figure(10)
    for xx0, yy0 in zip(x, y):
        plt.plot(xx0, yy0, 'bo')

        for xx1, yy1 in zip(x, y):
            plt.plot([xx0, xx1], [yy0, yy1], 'g:')
    plt.xlabel('Position (unitless)')
    plt.ylabel('Position (unitless)')
    # plt.show()
    plt.savefig('complete_graph.png')
    plt.close()

def build_distance_matrix(samples, home):
    """Entry point of the program."""
    # Instantiate the data problem.
    # data = create_data_model()
    waypoints = []
    np.random.seed(1)
    x = np.random.rand(samples, 1) * 100 - 50
    np.random.seed(2)
    y = np.random.rand(samples, 1) * 100 - 50
    id = [0, 1,   2,  3, 4, 5, 6,   7, 8,  9, 10]
    # x = [10, -10, 10, 2, 5, 6, 7,   9, -6, 1]
    # y = [1,  -5,  2,  5, 5, 7, 10, -3, 4, -10]
    waypoints_list = []
    for xx, yy in zip(x, y):
        waypoints.append(Waypoint(xx, yy, 50.0))
        waypoints_list.append([xx, yy])

    plot_complete_graph(x, y)

    # waypoints.append(home)

    waypoints.sort()
    # waypoints.insert(1, home)
    # home_index = waypoints.index(home)
    # home_index = waypoints.index(home)
    # ends = [home_index for i in range(num_vehicles)]

    # starts = []
    # while len(starts) < num_vehicles:
    #     candidate = np.random.choice()

    # print('ends', ends)

    # data = {'starts': [0], 'ends': ends, 'num_vehicles': num_vehicles}
    # data = {'starts': [0], 'ends': [1], 'num_vehicles': num_vehicles}
    num_points = len(waypoints)
    distance_matrix = [[0 for i in range(num_points)] for j in range(num_points)]
    for i in range(num_points):
        waypoint_a_x = waypoints[i].x
        waypoint_a_y = waypoints[i].y
        waypoint_a_z = waypoints[i].z
        for j in range(num_points):
            waypoint_b_x = waypoints[j].x
            waypoint_b_y = waypoints[j].y
            waypoint_b_z = waypoints[j].z
            dist = math.sqrt((waypoint_a_x - waypoint_b_x) ** 2 + (waypoint_a_y - waypoint_b_y) ** 2 )
            distance_matrix[j][i] = dist
    return distance_matrix, waypoints
