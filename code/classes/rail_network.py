import csv
import random
from typing import Dict, List, Tuple
from .station import Station
from .connection import Connection
from .route import Route

class RailNetwork:
    def __init__(self):
        """
        Initialize a RailNetwork object.
        """
        self.stations: Dict[str, Station] = {}
        self.connections: List[Connection] = []
        self.routes: List[Route] = []

    def load_stations(self, filename: str):
        """
        Load stations from a CSV file.
        
        Args:
            filename (str): Path to the CSV file containing station data
        """
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station = Station(row['station'], float(row['x']), float(row['y']))
                self.stations[station.name] = station

    def load_connections(self, filename: str):
        """
        Load connections from a CSV file.
        
        Args:
            filename (str): Path to the CSV file containing connection data
        """
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                connection = Connection(
                    row['station1'],
                    row['station2'],
                    int(row['distance'])
                )
                self.connections.append(connection)
                self.stations[connection.station1].add_connection(connection)
                self.stations[connection.station2].add_connection(connection)

    def create_route(self, start_station: str) -> Route:
        """
        Create a single route starting from the given station.
        
        Args:
            start_station (str): Name of the starting station
            
        Returns:
            Route: Created route object
        """
        route = Route()
        current_station = start_station
        
        while True:
            station = self.stations[current_station]
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

    def calculate_quality(self) -> float:
        """
        Calculate the quality score of the current solution.
        
        Returns:
            float: Quality score
        """
        total_connections = len(self.connections)
        used_connections = sum(1 for conn in self.connections if conn.used)
        p = used_connections / total_connections
        T = len(self.routes)
        Min = sum(route.total_time for route in self.routes)
        
        K = p * 10000 - (T * 100 + Min)
        return K

    def create_solution(self, max_routes: int = 7) -> float:
        """
        Create a complete solution with multiple routes.
        
        Args:
            max_routes (int): Maximum number of routes allowed
            
        Returns:
            float: Quality score of the created solution
        """
        # Reset all connections
        for conn in self.connections:
            conn.used = False
        self.routes.clear()
        
        # Create routes until we hit the maximum or use all connections
        while len(self.routes) < max_routes:
            unused_stations = [
                station.name for station in self.stations.values()
                if any(not conn.used for conn in station.connections.values())
            ]
            
            if not unused_stations:
                break
                
            start_station = random.choice(unused_stations)
            route = self.create_route(start_station)
            
            if route.connections_used:
                self.routes.append(route)
        
        return self.calculate_quality()

    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Find the best solution by trying multiple random solutions.
        
        Args:
            iterations (int): Number of random solutions to try
            
        Returns:
            Tuple[float, List[Route]]: Best quality score and corresponding routes
        """
        best_quality = float('-inf')
        best_routes = []
        
        for _ in range(iterations):
            quality = self.create_solution()
            if quality > best_quality:
                best_quality = quality
                best_routes = [Route() for _ in self.routes]
                for new_route, old_route in zip(best_routes, self.routes):
                    new_route.stations = old_route.stations.copy()
                    new_route.total_time = old_route.total_time
                    new_route.connections_used = old_route.connections_used.copy()
        
        return best_quality, best_routes