# heuristics.py
from typing import Dict
from classes.rail_network import RailNetwork
from classes.connection import Connection

class RouteHeuristics:
    def __init__(self, rail_network: RailNetwork):
        self.rail_network = rail_network
        
    def calculate_connection_value(self, connection: Connection, current_station: str, 
                                 current_route_time: int) -> float:
        """
        Calculate the value of adding this connection to the route.
        
        Args:
            connection: The connection being evaluated
            current_station: The current station we're at
            current_route_time: Current accumulated time in the route
            
        Returns:
            float: Score representing the value of using this connection
        """
        if connection.used:
            return float('-inf')  # Never reuse connections
            
        # Get destination station
        dest_station = connection.get_other_station(current_station)
        
        # Count unused connections reachable from destination
        nearby_unused = sum(
            1 for conn in self.rail_network.stations[dest_station].connections.values() 
            if not conn.used
        )
        
        # Heavily penalize routes that would force us to create a new route
        time_penalty = 0
        if current_route_time + connection.distance > 110:  # Leave buffer from 120 limit
            time_penalty = 100  # Equal to cost of new route in scoring function
            
        # Score = nearby_unused - (normalized_time_cost) - new_route_penalty
        return nearby_unused - (connection.distance / 180) - time_penalty
    
    def get_best_connection(self, current_station: str, current_route_time: int, 
                          visited_stations: set = None) -> tuple[Connection, float]:
        """
        Find the best available connection from current station.
        
        Args:
            current_station: Station to look from
            current_route_time: Current time accumulated in route
            visited_stations: Set of stations already visited (optional)
            
        Returns:
            tuple[Connection, float]: Best connection and its score, or (None, float('-inf'))
                                    if no valid connections exist
        """
        station = self.rail_network.stations[current_station]
        best_score = float('-inf')
        best_connection = None
        
        for dest, connection in station.connections.items():
            # Skip if we've visited this station (to avoid loops)
            if visited_stations and dest in visited_stations:
                continue
                
            # Skip if adding this would exceed time limit
            if current_route_time + connection.distance > 180:
                continue
                
            score = self.calculate_connection_value(
                connection, current_station, current_route_time
            )
            
            if score > best_score:
                best_score = score
                best_connection = connection
                
        return best_connection, best_score