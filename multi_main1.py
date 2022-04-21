"""Simple Vehicles Routing Problem."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from Waypoint import Waypoint
import math
import numpy as np

from matplotlib import pyplot as plt



def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
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
            print('route distance', route_distance, previous_index, index)
        plan_output += '{}\n'.format(manager.IndexToNode(index))

        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        routes.append(route)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))
    return routes


def plot_results(routes, waypoints, home, num_vehicles):
    x = []
    y = []
    for waypoint in waypoints:
        x.append(waypoint.x)
        y.append(waypoint.y)
    plt.plot(x, y, 'o')

    for i in range(num_vehicles):
        x = []
        y = []
        for route_index in routes[i]:
            x.append(waypoints[route_index].x)
            y.append(waypoints[route_index].y)
            print(route_index)
        x.append(home.x)
        y.append(home.y)
        plt.plot(x, y)
    plt.plot(0, 0, 'bx', markersize=10)
    plt.xlabel('Position (unitless)')
    plt.ylabel('Position (unitless)')
    plt.savefig("multi-agent1.png")

    # plt.show()




def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    # data = create_data_model()

    TIME_LIMIT  = 1
    waypoints = []
    num_vehicles = 2
    samples = 20
    np.random.seed(1)
    x = np.random.rand(samples, 1) * 100 - 50
    np.random.seed(2)
    y = np.random.rand(samples, 1) * 100 - 50
    id = [0, 1,   2,  3, 4, 5, 6,   7, 8,  9, 10]
    # x = [10, -10, 10, 2, 5, 6, 7,   9, -6, 1]
    # y = [1,  -5,  2,  5, 5, 7, 10, -3, 4, -10]

    for xx, yy in zip(x, y):
        waypoints.append(Waypoint(xx, yy, 50.0))
    home = Waypoint(0, 0, 50.0)

    waypoints.append(home)

    waypoints.sort()

    home_index = waypoints.index(home)
    ends = [home_index for i in range(num_vehicles)]

    starts = []
    # while len(starts) < num_vehicles:
    #     candidate = np.random.choice()

    print('ends', ends)

    data = {'starts': [0, 8], 'ends': ends, 'num_vehicles': num_vehicles}
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
    for line in data['distance_matrix']:
        print(line)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

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
        routes = print_solution(data, manager, routing, solution)
        plot_results(routes, waypoints, home, num_vehicles)


if __name__ == '__main__':
    main()
