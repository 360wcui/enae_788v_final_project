"""Simple Vehicles Routing Problem."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from Waypoint import Waypoint
import math
import numpy as np

from matplotlib import pyplot as plt

home = Waypoint(0, 0, 50.0)

TIME_LIMIT = 1
num_vehicles = 1
samples = 20

def plot_results(routes, waypoints, home, num_vehicles):
    x = []
    y = []
    for waypoint in waypoints:
        x.append(waypoint.x)
        y.append(waypoint.y)
    plt.plot(x, y, 'o')
    first_x = None
    first_y = None
    last_x = None
    last_y = None
    current_x = None
    current_y = None
    distance = 0

    for i in range(num_vehicles):
        x = []
        y = []
        print(routes[i])
        for route_index in routes[i]:
            if first_x is None:
                first_x = waypoints[route_index].x
                first_y = waypoints[route_index].y
            last_x = current_x
            last_y = current_y
            current_x = waypoints[route_index].x
            current_y = waypoints[route_index].y
            if last_x is not None and last_y is not None:
                # print('haha', last_x, last_y, current_x, current_y)
                step = np.sqrt((current_x - last_x) ** 2 + (current_y - last_y) ** 2)
                distance += step
                print(distance, step)
            x.append(waypoints[route_index].x)
            y.append(waypoints[route_index].y)
            # print(route_index)
        # x.append(home.x)
        # y.append(home.y)
        plt.plot(x, y)
        # last_x = current_x
        # last_y = current_y
        # current_x = home.x
        # current_y = home.y
        # step = np.sqrt((current_x - last_x) ** 2 + (current_y - last_y) ** 2)
        # distance += step



    # plt.plot(0, 0, 'bx', markersize=10)

    distance += np.sqrt((current_x - first_x) ** 2 + (current_y - first_y) ** 2)
    print("manually caluclated distance", distance)
    plt.savefig("result1.png")
    plt.show()




def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    # data = create_data_model()

    waypoints = []
    np.random.seed(1)
    x = np.random.rand(samples, 1) * 100 - 50
    np.random.seed(2)
    y = np.random.rand(samples, 1) * 100 - 50
    best_route_distance = 999
    id = [0, 1,   2,  3, 4, 5, 6,   7, 8,  9, 10]
    # x = [10, -10, 10, 2, 5, 6, 7,   9, -6, 1]
    # y = [1,  -5,  2,  5, 5, 7, 10, -3, 4, -10]

    for xx, yy in zip(x, y):
        # print(xx, yy)
        waypoints.append(Waypoint(xx, yy, 50.0))

    waypoints.sort()

    ends = [1]
    starts = [0]

    data = {'starts': starts, 'ends': ends, 'num_vehicles': num_vehicles}
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
    data['distance_matrix'] = distance_matrix

    for line in distance_matrix:
        print(line)

    routes = [[0, 3, 12, 16, 19, 17, 15, 13, 9, 8, 11, 10, 14, 18, 6, 7, 5, 1, 2, 4, 0]] # held karp
    routes = [[0, 3, 12, 13, 9, 11, 15, 17, 16, 19, 18, 14, 10, 8, 4, 2, 5, 7, 6, 1, 0]] # christofides
    # routes = [[0, 4, 2, 1, 5, 7, 6, 18, 14, 10, 11, 8, 9, 13, 15, 17, 19, 16, 12, 3, 0]] # prob

        # routes, max_route_distance = print_solution(data, manager, routing, solution)
    home_index = ends[0]
    home = waypoints[home_index]
    print(home_index, home)

    plot_results(routes, waypoints, home, num_vehicles)

    return waypoints, data


if __name__ == '__main__':
    main()
