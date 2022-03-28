"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

TIME_LIMIT = 3

def create_data_model():
    """Stores the data for the problem."""
    data= {}
    data['distance_matrix'] = [[1 for i in range(9)] for j in range(9)]
    print(data['distance_matrix'])

    # data['distance_matrix'] = [
    #     [
    #         0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
    #         468, 776, 662
    #     ],
    #     [
    #         548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 684, 594, 480, 674,
    #         616, 868, 510
    #     ],
    #     [
    #         776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 578, 664,
    #         830, 788, 1252, 754
    #     ],
    #     [
    #         696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 532, 514, 628, 822,
    #         664, 560, 458
    #     ],
    #     [
    #         582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 618, 400, 514, 708,
    #         1050, 674, 544
    #     ],
    #     [
    #         274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
    #         514, 1050, 708
    #     ],
    #     [
    #         502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
    #         514, 578, 480
    #     ],
    #     [
    #         194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
    #         662, 742, 856
    #     ],
    #     [
    #         308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
    #         320, 684, 514
    #     ],
    #     [
    #         194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
    #         274, 810, 468
    #     ],
    #     [
    #         536, 684, 400, 532, 618, 582, 354, 730, 388, 342, 0, 878, 764,
    #         730, 388, 552, 354
    #     ],
    #     [
    #         502, 594, 578, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
    #         308, 650, 274, 844
    #     ],
    #     [
    #         388, 480, 664, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
    #         536, 388, 730
    #     ],
    #     [
    #         354, 674, 830, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
    #         342, 422, 536
    #     ],
    #     [
    #         468, 616, 788, 664, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
    #         342, 0, 764, 194
    #     ],
    #     [
    #         776, 868, 1252, 560, 674, 1050, 578, 742, 684, 810, 552, 274,
    #         388, 422, 764, 0, 798
    #     ],
    #     [
    #         662, 510, 754, 458, 544, 708, 480, 856, 514, 468, 354, 844, 730,
    #         536, 194, 798, 0
    #     ],
    # ]
    data['num_vehicles'] = 2
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
    print('optimal routes', optimal_routes)
    print('Maximum of the route distances: {}m'.format(max_route_distance))




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
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
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
