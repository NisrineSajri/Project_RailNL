import csv
import random
from typing import Dict, List, Tuple, Set
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
                    float(row['distance'])
                )
                self.connections.append(connection)
                self.stations[connection.station1].add_connection(connection)
                self.stations[connection.station2].add_connection(connection)

    def get_used_connections(self) -> Set[Connection]:
        """
        Get set of all unique connections used across all routes.
        
        Returns:
            Set[Connection]: Set of unique connections that are used
        """
        used_connections = set()
        for route in self.routes:
            used_connections.update(route.connections_used)
        return used_connections

    def calculate_quality(self) -> float:
        """
        Calculate the quality score of the current solution using unique connections.
        
        Returns:
            float: Quality score based on the formula K = p * 10000 - (T * 100 + Min)
            where:
            - p is the proportion of connections used
            - T is the number of routes
            - Min is the total time of all routes
        """
        total_connections = len(self.connections)
        used_connections = len(self.get_used_connections())
        p = used_connections / total_connections
        T = len(self.routes)
        Min = sum(route.total_time for route in self.routes)
        
        K = p * 10000 - (T * 100 + Min)
        return K

    def sync_connection_states(self):
        """
        Synchronize connection.used flags with route.connections_used sets.
        Ensures that the connection.used flags match what's actually used in routes.
        """
        # First reset all connections
        for conn in self.connections:
            conn.used = False
            
        # Then mark used connections based on routes
        used_conns = self.get_used_connections()
        for conn in used_conns:
            conn.used = True

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
        route.stations = [start_station]
        
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
            route.stations.append(current_station)
            
        return route

    def reset(self):
        """
        Reset the network state by clearing all routes and connection usage.
        """
        self.routes.clear()
        for conn in self.connections:
            conn.used = False