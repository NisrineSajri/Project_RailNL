from typing import List, Set
from .connection import Connection

class Route:
    def __init__(self, time_limit: int = 180):  # Standaard naar de grootste tijdslimiet
        """
        Initialiseer een Route object.
        
        Args:
            time_limit: Maximale tijdslimiet voor de route in minuten
        """
        self.stations: List[str] = []
        self.total_time = 0
        self.connections_used: Set[Connection] = set()
        self.time_limit = time_limit

    def add_connection(self, connection: Connection) -> bool:
        """
        Voeg een verbinding toe aan de route als deze de tijdslimiet niet overschrijdt.
        
        Args:
            connection (Connection): Verbinding die aan de route moet worden toegevoegd
            
        Retourneert:
            bool: True als de verbinding succesvol werd toegevoegd, False anders
        """
        if self.total_time + connection.distance > self.time_limit:
            return False

        self.total_time += connection.distance
        if not self.stations:
            self.stations.extend([connection.station1, connection.station2])
        else:
            self.stations.append(connection.get_other_station(self.stations[-1]))
        self.connections_used.add(connection)
        connection.used = True
        return True

    def __str__(self) -> str:
        """
        String representatie van de Route.
        
        Retourneert:
            str: Een string die de route beschrijft
        """
        return f"Route({' -> '.join(self.stations)}, {self.total_time} min)"
