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

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    # print(f'Objective: {solution.ObjectiveValue()}')
    routes = []
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        route = []
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        node = manager.IndexToNode(index)
        # route.append(node)
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            node = manager.IndexToNode(index) # node = index + 1 for 2nd vehicle,  node = index for 1st vehicle, node is the actual index of self.waypoints.
            route.append(node)
            # print('haha', index, node)
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            # print('route distance', route_distance, previous_index, index)
        plan_output += '{}\n'.format(manager.IndexToNode(index))

        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        routes.append(route)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))
    return routes, max_route_distance


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
                distance += np.sqrt((current_x - last_x) ** 2 + (current_y - last_y) ** 2)

            x.append(waypoints[route_index].x)
            y.append(waypoints[route_index].y)
            # print(route_index)
        x.append(home.x)
        y.append(home.y)
        plt.plot(x, y)
        last_x = current_x
        last_y = current_y
        current_x = home.x
        current_y = home.y
        distance += np.sqrt((current_x - last_x) ** 2 + (current_y - last_y) ** 2)
        print("manually caluclated distance", distance)
    # plt.plot(0, 0, 'bx', markersize=10)

    distance += np.sqrt((current_x - first_x) ** 2 + (current_y - first_y) ** 2)

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

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    for i in range(samples // 2 - 1):
        ends = [i]
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

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                               data['num_vehicles'], data['starts'],
                                               data['ends'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        # Create and register a transit callback.


        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Distance constraint.
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            1,  # no slack
            1000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(10)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        # https://developers.google.com/optimization/routing/routing_options#local_search_options
        search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = TIME_LIMIT
        search_parameters.log_search = True

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            routes, max_route_distance = print_solution(data, manager, routing, solution)
            if max_route_distance < best_route_distance:
                home_index = ends[0]
                home = waypoints[home_index]
                print(home_index, home)

                best_route_distance =  max_route_distance
                plot_results(routes, waypoints, home, num_vehicles)
        print('best_route_distance', best_route_distance)

    return waypoints, data


if __name__ == '__main__':
    main()
