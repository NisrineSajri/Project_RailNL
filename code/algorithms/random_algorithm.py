import random
from typing import List, Tuple
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from classes.rail_network import RailNetwork
from classes.route import Route
from classes.connection import Connection
from constants import STATIONS_FILE, CONNECTIONS_FILE

class RandomAlgorithm:
    def __init__(self, rail_network: RailNetwork):
        self.rail_network = rail_network
        
    def create_route(self, start_station: str, time_limit: int = 120) -> Route:
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

    def create_solution(self, max_routes: int = 7) -> float:
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

if __name__ == "__main__":
    try:
        network = RailNetwork()
        network.load_stations(STATIONS_FILE)
        network.load_connections(CONNECTIONS_FILE)
        
        random_algo = RandomAlgorithm(network)
        best_quality, best_routes = random_algo.find_best_solution(iterations=100)
        
        from classes.solution_statistics import SolutionStatistics
        stats = SolutionStatistics(best_quality, best_routes)
        stats.print_stats()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Stations file path: {STATIONS_FILE}")
        print(f"Connections file path: {CONNECTIONS_FILE}")