from typing import List, Set
from .connection import Connection

class Route:
    def __init__(self, time_limit: int = 180):  # Default to largest time limit
        """
        Initialize a Route object.
        
        Args:
            time_limit: Maximum time limit for the route in minutes
        """
        self.stations: List[str] = []
        self.total_time = 0
        self.connections_used: Set[Connection] = set()
        self.time_limit = time_limit

    def add_connection(self, connection: Connection) -> bool:
        """
        Add a connection to the route if it doesn't exceed the time limit.
        
        Args:
            connection (Connection): Connection to add to the route
            
        Returns:
            bool: True if connection was added successfully, False otherwise
        """
        if self.total_time + connection.distance > self.time_limit:
            return False

        self.total_time += connection.distance
        if not self.stations:
            self.stations.extend([connection.station1, connection.station2])
        else:
            last_station = self.stations[-1]
            if last_station == connection.station1:
                self.stations.append(connection.station2)
            elif last_station == connection.station2:
                self.stations.append(connection.station1)
            else:
                return False
            self.connections_used.add(connection)
        connection.used = True
        return True

    def __str__(self) -> str:
        """
        String representation of the Route.
        
        Returns:
            str: String describing the route
        """
        return f"Route({' -> '.join(self.stations)}, {self.total_time} min)"