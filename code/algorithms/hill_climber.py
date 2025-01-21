import random
from copy import deepcopy
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route
from algorithms.greedy import GreedyAlgorithm

class HillClimber:
    def __init__(self, network: RailNetwork, initial_routes: List[Route] = None, time_limit: int = 120, max_routes: int = 7):
        """
        Initialize the HillClimber with an initial solution (greedy algorithm).
        Args:
            network: The rail network to work with
            initial_routes: Optional initial solution, if not provided uses GreedyAlgorithm
            time_limit: Maximum time limit for routes in minutes
            max_routes: Maximum number of routes allowed
        """
        self.network = network
        self.max_routes = max_routes
        self.max_time = time_limit

        # If no initial solution is provided, use GreedyAlgorithm
        if initial_routes is None:
            greedy = GreedyAlgorithm(network, time_limit=time_limit, max_routes=max_routes)
            _, self.current_routes = greedy.find_best_solution()
        else:
            self.current_routes = self.copy_routes(initial_routes)

        # Sync initial network state
        self.network.sync_connection_states()

    def copy_routes(self, routes: List[Route]) -> List[Route]:
        """Make a deep copy of routes to avoid modifying the originals."""
        return deepcopy(routes)

    def modify_route(self, route: Route) -> Route:
        """
        Make a small modification to a route.
        Possible modifications (random):
        1. Remove last connection and try a different path
        2. Remove random connection and rebuild from that point
        3. Start from a different station in the route
        """
        optie = random.choice([1, 2, 3])
            
        # Choose start point based on option type
        if optie == 1:
            # Remove last connection
            if len(route.stations) > 2:
                # Choose second to last station as start point
                start_idx = len(route.stations) - 2
                start_station = route.stations[start_idx]
            else:
                start_station = route.stations[0]
        
        elif optie == 2:
            # Remove random connection
            if len(route.stations) > 2:
                start_station = random.choice(route.stations[:-1])
            else:
                start_station = route.stations[0]

        else:  # optie == 3
            # Start from different station in route
            start_station = random.choice(route.stations)

        # Create new route using greedy approach
        greedy_algorithm = GreedyAlgorithm(self.network)
        new_route = greedy_algorithm.create_route(self.network.stations[start_station])
        
        return new_route

    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Execute hill climbing algorithm to find a better solution.

        Args:
            iterations: Number of iterations to perform

        Returns:
            Tuple[float, List[Route]]: Best quality score and corresponding routes
        """
        # Get initial quality
        best_quality = self.network.calculate_quality()
        best_routes = self.copy_routes(self.current_routes)
        
        i = 0
        while i < iterations:
            # Choose random route to modify
            route_idx = random.randrange(len(self.current_routes))
            old_route = self.current_routes[route_idx]
            
            # Remember old connections and reset their states
            old_connections = set(old_route.connections_used)
            for conn in old_connections:
                conn.used = False
            
            # Try modification
            new_route = self.modify_route(old_route)
            
            # Update current solution and sync network state
            self.current_routes[route_idx] = new_route
            self.network.sync_connection_states()

            # Calculate new quality
            new_quality = self.network.calculate_quality()

            # Accept if better, else revert
            if new_quality > best_quality:
                best_quality = new_quality
                best_routes = self.copy_routes(self.current_routes)
            else:
                # Revert to old route and restore connection states
                self.current_routes[route_idx] = old_route
                self.network.sync_connection_states()
            
            i += 1

        return best_quality, best_routes