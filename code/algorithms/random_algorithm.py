import random
from typing import List, Tuple

from classes.rail_network import RailNetwork
from classes.route import Route

class RandomAlgorithm:
    def __init__(self, rail_network: RailNetwork):
        self.rail_network = rail_network
        
    def create_route(self, start_station: str, time_limit: int = 180) -> Route:
        """
        Create a single route starting from the given station.
        
        Args:
            start_station (str): Starting station name
            time_limit (int): Maximum route time in minutes (default 120)
            
        Returns:
            Route: Created route object
        """
        route = Route()
        current_station = start_station
        route.stations = [start_station]
        
        while True:
            station = self.rail_network.stations[current_station]
            possible_connections = [
                conn for dest, conn in station.connections.items()
                if not conn.used and route.total_time + conn.distance <= time_limit
            ]
            
            if not possible_connections:
                break
                
            connection = random.choice(possible_connections)
            if not route.add_connection(connection):
                break
                
            current_station = connection.get_other_station(current_station)
            route.stations.append(current_station)
            
        return route

    def create_solution(self, max_routes: int = 20) -> float:
        """
        Create a complete solution with multiple routes.
        
        Args:
            max_routes (int): Maximum number of routes allowed
            
        Returns:
            float: Quality score of the solution
        """
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        routes_created = 0
        all_stations = list(self.rail_network.stations.keys())
        
        while routes_created < max_routes:
            unused_stations = [
                station.name for station in self.rail_network.stations.values()
                if any(not conn.used for conn in station.connections.values())
            ]
            
            if not unused_stations:
                break
                
            start_station = random.choice(unused_stations)
            route = self.create_route(start_station)
            
            if route.connections_used:
                for conn in route.connections_used:
                    conn.used = True
                self.rail_network.routes.append(route)
                routes_created += 1
        
        return self.rail_network.calculate_quality()

    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Find the best solution by trying multiple random solutions.
        
        Args:
            iterations (int): Number of attempts to make
            
        Returns:
            tuple[float, List[Route]]: Best quality score and corresponding routes
        """
        best_quality = float('-inf')
        best_routes = []
        
        for i in range(iterations):
            quality = self.create_solution()
            if quality > best_quality:
                best_quality = quality
                best_routes = [Route() for _ in self.rail_network.routes]
                for new_route, old_route in zip(best_routes, self.rail_network.routes):
                    new_route.stations = old_route.stations.copy()
                    new_route.total_time = old_route.total_time
                    new_route.connections_used = old_route.connections_used.copy()
        
        return best_quality, best_routes