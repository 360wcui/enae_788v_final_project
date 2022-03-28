"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
TIME_LIMIT = 1

def create_data_model():
    """Stores the data for the problem."""
    data= {}
    point0 = {'x': 103,'y': 23.35}
    point1 = {'x': 20, 'y': 20}
    point2 = {'x': 30, 'y': 30}
    points = [point0, point1, point2]
    data['distance_matrix'] = [[1 for i in range(3)] for j in range(3)]
    for i in range(len(points)):
        for j in range(len(points)):
            pointA = points[i]
            pointB = points[j]
            print(pointA, pointB)
            data['distance_matrix'][i][j] = math.sqrt((pointA['x'] - pointB['x']) ** 2 + (pointA['y'] - pointB['y']) ** 2)

    print(data['distance_matrix'])


    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


# [START solution_printer]
def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    routes = []
    for vehicle_id in range(data['num_vehicles']):
        route = []
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        # route.append(index)
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            route.append(index)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        route.append(routing.Start(vehicle_id))
        routes.append(route)

        plan_output += 'haha{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance1 of the route: {}m\n'.format(route_distance)
        print('plan-output', plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    optimal_routes = routes
    # print('optimal routes', optimal_routes)
    # print('Maximum of the route distances: {}m'.format(max_route_distance))




def main():

    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    matrix = data['distance_matrix']
    for row in matrix:
        print(row)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

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
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(10)

    # Setting first solution heuristic.
    # search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.first_solution_strategy = (
    #     routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC)
    #     # routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = TIME_LIMIT
    search_parameters.log_search = False

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')


if __name__ == '__main__':
    main()
