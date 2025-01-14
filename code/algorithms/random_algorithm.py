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

class RandomAlgorithm:
    def __init__(self, rail_network):
        self.rail_network = rail_network
        
    def create_route(self, start_station: str) -> Route:
        """
        Create a single route starting from the given station.
        """
        route = Route()
        current_station = start_station
        
        while True:
            station = self.rail_network.stations[current_station]
            possible_connections = [
                conn for dest, conn in station.connections.items()
                if not conn.used and route.total_time + conn.distance <= 120
            ]
            
            if not possible_connections:
                break
                
            connection = random.choice(possible_connections)
            if not route.add_connection(connection):
                break
                
            current_station = connection.get_other_station(current_station)
            
        return route

    def create_solution(self, max_routes: int = 7) -> float:
        """
        Create a complete solution with multiple routes.
        """
        # Reset all connections
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        # Create routes until we hit the maximum or use all connections
        while len(self.rail_network.routes) < max_routes:
            unused_stations = [
                station.name for station in self.rail_network.stations.values()
                if any(not conn.used for conn in station.connections.values())
            ]
            
            if not unused_stations:
                break
                
            start_station = random.choice(unused_stations)
            route = self.create_route(start_station)
            
            if route.connections_used:
                self.rail_network.routes.append(route)
        
        return self.rail_network.calculate_quality()

    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Find the best solution by trying multiple random solutions.
        """
        best_quality = float('-inf')
        best_routes = []
        
        for _ in range(iterations):
            quality = self.create_solution()
            if quality > best_quality:
                best_quality = quality
                best_routes = [Route() for _ in self.rail_network.routes]
                for new_route, old_route in zip(best_routes, self.rail_network.routes):
                    new_route.stations = old_route.stations.copy()
                    new_route.total_time = old_route.total_time
                    new_route.connections_used = old_route.connections_used.copy()
        
        return best_quality, best_routes

def print_solution_stats(quality: float, routes: List[Route]):
    """Print detailed statistics about the solution"""
    total_time = sum(route.total_time for route in routes)
    coverage_cost = len(routes) * 100 + total_time
    p = (quality + coverage_cost) / 10000
    
    print("\nSolution Statistics:")
    print(f"Quality Score (K): {quality:.2f}")
    print(f"Number of routes (T): {len(routes)}")
    print(f"Total time (Min): {total_time} minutes")
    print(f"Connection coverage (p): {p:.4f} ({p*100:.1f}%)")
    
    print("\nRoutes:")
    for i, route in enumerate(routes, 1):
        print(f"{i}. {route}")

if __name__ == "__main__":
    # Get the root directory path
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    STATIONS_FILE = os.path.join(DATA_DIR, "StationsHolland.csv")
    CONNECTIONS_FILE = os.path.join(DATA_DIR, "ConnectiesHolland.csv")
    
    # Create and initialize the network
    network = RailNetwork()
    network.load_stations(STATIONS_FILE)
    network.load_connections(CONNECTIONS_FILE)
    
    # Run the random algorithm
    random_algo = RandomAlgorithm(network)
    best_quality, best_routes = random_algo.find_best_solution(iterations=1000)
    
    # Print the results
    print_solution_stats(best_quality, best_routes)