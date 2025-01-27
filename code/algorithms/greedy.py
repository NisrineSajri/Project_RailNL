# greedy.py
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.station import Station

class GreedyAlgorithm:
    def __init__(self, network: RailNetwork, time_limit: int = 120, max_routes: int = 7):
        """
        Initialiseer de Greedy-algoritmeklasse.
        
        Args:
            network (RailNetwork): Het railnetwerk waarmee gewerkt wordt.
            time_limit (int, default 120): Maximale tijdslimiet voor routes in minuten.
            max_routes (int, default 7): Maximale aantal routes.
        """
        # Bind het netwerk aan de Greedy-algoritmeklasse
        self.network = network  
        
        # Gebruik het maximale aantal routes
        self.max_routes = max_routes 
        
        # Gebruik de tijdslimiet
        self.max_time = time_limit  

    def get_most_connections(self) -> List[Station]:
        """
        Verkrijg een lijst van stations gesorteerd op het aantal verbindingen, van de minste naar de meeste.
        
        Returns:
            List[Station]: Lijst van stations gesorteerd op het aantal verbindingen.
        """
        # Verkrijg alle stations uit het netwerk
        stations = list(self.network.stations.values())
        
        # Sorteer stations op basis van het aantal verbindingen in oplopende volgorde
        stations.sort(key=lambda station: len(station.connections), reverse=False)
        
        return stations

    def create_route(self, start_station: Station) -> Route:
        """
        Maak een enkele route die begint bij het opgegeven station.
        
        Args:
            start_station (Station): Het station waarmee de route begint.
        
        Returns:
            Route: De gemaakte route.
        """
        # Geef de tijdslimiet door
        route = Route(time_limit=self.max_time)
        current_station = start_station.name

        # Houd bij welke stations al bezocht zijn in deze route
        visited_stations = set()  

        while True:
            station = self.network.stations[current_station]

            # Markeer het station als bezocht
            visited_stations.add(current_station)  

            # Verkrijg alle geldige verbindingen die:
            # 1. Nog niet gebruikt zijn.
            # 2. De maximale tijdslimiet niet overschrijden.
            # 3. Naar stations leiden die nog niet bezocht zijn in deze route.
            for _, conn in station.connections.items():
                if not conn.used and route.total_time + conn.distance <= self.max_time:
                    other_station = conn.get_other_station(current_station)
                    if other_station not in visited_stations:
                        # Voeg de ongebruikte verbinding direct toe aan de route
                        if route.add_connection(conn):
                            # Als verbinding succesvol is toegevoegd, werk huidige station bij
                            current_station = other_station
                            # Ga verder met de volgende verbinding na toevoeging
                            break  
            else:
                # Geen geldige verbindingen gevonden; eindig de route
                break

        return route

    def runGreedy(self) -> float:
        """
        Voer het greedy-algoritme uit om routes te creëren op basis van een gesorteerde lijst van stations.
        
        Returns:
            float: De kwaliteit van de gemaakte routes, berekend door de functie `calculate_quality` van het netwerk.
        """
        # Reset alle verbindingen om mijn connecties te selecteren
        for conn in self.network.connections:
            conn.used = False
        self.network.routes.clear()

        # Verkrijg de gesorteerde lijst van stations op basis van het aantal verbindingen
        sorted_stations = self.get_most_connections()

        # Houd bij welke stations al als startpunt zijn gebruikt
        used_stations = set()  

        for start_station in sorted_stations:
            # Controleer of het station beschikbare verbindingen heeft
            if start_station.name in used_stations:
                # Sla station over als het al als startpunt is gebruikt
                continue  

            # Markeer het station als gebruikt
            used_stations.add(start_station.name)

            # Maak een route die begint bij het huidige station
            route = self.create_route(start_station)

            # Voeg de route toe aan het netwerk als het verbindingen bevat
            if route.connections_used:
                self.network.routes.append(route)

            # Controleer of het maximale aantal routes bereikt is
            if len(self.network.routes) >= self.max_routes:
                break

        # Bereken en retourneer de kwaliteit van de gemaakte routes
        return self.network.calculate_quality()

    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Vind de beste oplossing (enkele iteratie, aangezien het deterministisch is).
        
        Args:
            iterations (int, default 1): Het aantal iteraties voor de berekening (wordt hier niet gebruikt, omdat het algoritme deterministisch is).
        
        Returns:
            Tuple[float, List[Route]]: Een tuple met de kwaliteitsscore en de bijbehorende lijst van routes.
        """
        quality = self.runGreedy()
        best_routes = [Route() for _ in self.network.routes]
        for new_route, old_route in zip(best_routes, self.network.routes):
            new_route.stations = old_route.stations.copy()
            new_route.total_time = old_route.total_time
            new_route.connections_used = old_route.connections_used.copy()
        
        return quality, best_routes
