import csv
import random
from typing import Dict, List, Tuple, Set
from .station import Station
from .connection import Connection
from .route import Route

class RailNetwork:
    def __init__(self):
        """
        Initialiseer een RailNetwork object.
        """
        # Opslag voor stations
        self.stations: Dict[str, Station] = {} 
        
        # Opslag voor verbindingen 
        self.connections: List[Connection] = []  
        
        # Opslag voor routes
        self.routes: List[Route] = []  

    def load_stations(self, filename: str):
        """
        Laad stations uit een CSV-bestand.

        Args:
            filename (str): Pad naar het CSV-bestand met stationgegevens
        """
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station = Station(row['station'], float(row['x']), float(row['y']))
                self.stations[station.name] = station

    def load_connections(self, filename: str):
        """
        Laad verbindingen uit een CSV-bestand.

        Args:
            filename (str): Pad naar het CSV-bestand met verbindingsgegevens
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
        Verkrijg de set van alle unieke verbindingen die in de routes worden gebruikt.

        Return:
            Set[Connection]: Set van unieke verbindingen die worden gebruikt
        """
        used_connections = set()
        for route in self.routes:
            used_connections.update(route.connections_used)
        return used_connections

    def calculate_quality(self) -> float:
        """
        Bereken de kwaliteitscore van de huidige oplossing op basis van unieke verbindingen.

        Return:
            float: Kwaliteitsscore op basis van de formule K = p * 10000 - (T * 100 + Min)
            Waarbij:
            - p de proportie van gebruikte verbindingen is
            - T het aantal routes is
            - Min de totale tijd van alle routes is
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
        Synchroniseer de `used` status van verbindingen met de gebruikte verbindingen in de routes.
        Zorgt ervoor dat de 'used' vlaggen overeenkomen met wat daadwerkelijk in de routes wordt gebruikt.
        """
        # Reset eerst alle verbindingen
        for conn in self.connections:
            conn.used = False
            
        # Markeer daarna de gebruikte verbindingen
        used_conns = self.get_used_connections()
        for conn in used_conns:
            conn.used = True

    def create_route(self, start_station: str) -> Route:
        """
        Maak een enkele route die begint bij het opgegeven station.

        Args:
            start_station (str): Naam van het startstation

        Return:
            Route: Gecreëerd route-object
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
        Reset het netwerk door alle routes en verbindinggebruik te wissen.
        """
        self.routes.clear()
        for conn in self.connections:
            conn.used = False
