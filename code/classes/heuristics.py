from typing import Dict
from classes.rail_network import RailNetwork
from classes.connection import Connection

class RouteHeuristics:
    def __init__(self, rail_network: RailNetwork, time_limit: int = 120):
        """
        Initialiseer RouteHeuristics met een configureerbare tijdslimiet.
        
        Args:
            rail_network: Het spoornetwerk om mee te werken
            time_limit: Maximale tijdslimiet voor routes in minuten
        """
        self.rail_network = rail_network
        self.time_limit = time_limit
        
    def calculate_connection_value(self, connection: Connection, current_station: str, 
                                 current_route_time: int) -> float:
        """
        Bereken de waarde van het toevoegen van deze verbinding aan de route.
        
        Args:
            connection: De verbinding die geëvalueerd wordt
            current_station: Het huidige station waar we ons bevinden
            current_route_time: Huidige opgetelde tijd in de route
            
        Returns:
            float: Score die de waarde van het gebruik van deze verbinding weergeeft
        """
        if connection.used:
            # Nooit verbindingen hergebruiken
            return float('-inf')  
            
        # Haal het bestemmingsstation op
        dest_station = connection.get_other_station(current_station)
        
        # Tel ongebruikte verbindingen die bereikbaar zijn vanaf het bestemmingsstation
        nearby_unused = sum(
            1 for conn in self.rail_network.stations[dest_station].connections.values() 
            if not conn.used
        )
        
        # Zwaar bestraffen als routes ons zouden dwingen een nieuwe route te creëren
        time_penalty = 0

        # Laat een buffer van 10 minuten vanaf de limiet
        buffer_time = self.time_limit - 10  
        if current_route_time + connection.distance > buffer_time:
            # Gelijk aan de kosten van een nieuwe route in de scoringsfunctie
            time_penalty = 100  
            
        # Score = nearby_unused - (genormaliseerde tijdskosten) - straf voor nieuwe route
        return nearby_unused - (connection.distance / self.time_limit) - time_penalty
    
    def get_best_connection(self, current_station: str, current_route_time: int, 
                          visited_stations: set = None) -> tuple[Connection, float]:
        """
        Vind de beste beschikbare verbinding vanaf het huidige station.
        
        Args:
            current_station: Station waar vandaan gezocht wordt
            current_route_time: Huidige opgetelde tijd in de route
            visited_stations: Set van stations die al bezocht zijn (optioneel)
            
        Returns:
            tuple[Connection, float]: Beste verbinding en de score ervan, of (None, float('-inf'))
                                    als er geen geldige verbindingen bestaan
        """
        station = self.rail_network.stations[current_station]
        best_score = float('-inf')
        best_connection = None
        
        for dest, connection in station.connections.items():
            # Overslaan als we dit station al bezocht hebben (om lussen te vermijden)
            if visited_stations and dest in visited_stations:
                continue
                
            # Overslaan als het toevoegen hiervan de tijdslimiet zou overschrijden
            if current_route_time + connection.distance > self.time_limit:
                continue
                
            score = self.calculate_connection_value(
                connection, current_station, current_route_time
            )
            
            if score > best_score:
                best_score = score
                best_connection = connection
                
        return best_connection, best_score