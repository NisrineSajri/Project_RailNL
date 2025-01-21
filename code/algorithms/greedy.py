# greedy.py
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.station import Station

class GreedyAlgorithm:
    def __init__(self, network: RailNetwork, time_limit: int = 120, max_routes: int = 7):
        """
        Initialize the Greedy class.
        Args:
            network: The rail network to work with
            time_limit: Maximum time limit for routes in minutes
            max_routes: Maximum number of routes allowed
        """
        self.network = network  # Bind the network to the Greedy class
        self.max_routes = max_routes  # Use the max_routes from config
        self.max_time = time_limit  # Use the time limit from config

    def get_most_connections(self) -> list[Station]:
        """
        Get a list of stations sorted by the number of connections, from most to least.

        Returns:
            list[Station]: List of stations sorted by number of connections. minste connect
        """
        # Get all stations from the network
        stations = list(self.network.stations.values())
        
        # Sort all stations by the number of connections in descending order
        stations.sort(key=lambda station: len(station.connections), reverse=False)
        
        return stations

    def create_route(self, start_station: Station) -> Route:
        """Creates a single route starting from the given station."""
        route = Route(time_limit=self.max_time)  # Pass the time limit
        current_station = start_station.name
        visited_stations = set()  # Keep track of stations visited in this route

        while True:
            station = self.network.stations[current_station]
            visited_stations.add(current_station)  # Mark the station as visited

            # Get all valid connections that:
            # 1. Have not been used.
            # 2. Do not exceed the max time.
            # 3. Lead to stations not already visited in this route.
            for _, conn in station.connections.items():
                if not conn.used and route.total_time + conn.distance <= self.max_time:
                    other_station = conn.get_other_station(current_station)
                    if other_station not in visited_stations:
                        # Directly add the unused connection to the route
                        if route.add_connection(conn):
                            # If the connection is successfully added, update the current station
                            current_station = other_station
                            break  # Move on to the next connection after adding
            else:
                # If no valid connection is found, end the route
                break

        return route


    def runGreedy(self):
        """
        Run the greedy algorithm to create routes using a sorted list of stations.
        """
        # Reset all connections om mijn connecties te selecteren
        for conn in self.network.connections:
            conn.used = False
        self.network.routes.clear()

        # Get the sorted list of stations by number of connections
        sorted_stations = self.get_most_connections()
        used_stations = set()  # Track stations already used as starting points 

        for start_station in sorted_stations:
            # Check if the station has available connections
            if start_station.name in used_stations:
                continue  # Skip this station if it has already been used as a starting point

            # Mark the station as used
            used_stations.add(start_station.name)

            # Create a route starting from the current station
            route = self.create_route(start_station)

            # Add the route to the network if it contains connections
            if route.connections_used:
                self.network.routes.append(route)

            # Check if the maximum number of routes has been reached
            if len(self.network.routes) >= self.max_routes:
                break

        # Calculate and return quality
        return self.network.calculate_quality()

    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Find best solution (single iteration since deterministic).
        
        Args:
            iterations: Kept for API compatibility
            
        Returns:
            Tuple[float, List[Route]]: Quality score and corresponding routes
        """
        quality = self.runGreedy()
        best_routes = [Route() for _ in self.network.routes]
        for new_route, old_route in zip(best_routes, self.network.routes):
            new_route.stations = old_route.stations.copy()
            new_route.total_time = old_route.total_time
            new_route.connections_used = old_route.connections_used.copy()
        
        return quality, best_routes