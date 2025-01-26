# Hill_climber.py
import random
from copy import deepcopy
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route

class HillClimber:
    def __init__(self, network: RailNetwork, time_limit: int = 120, max_routes: int = 7, seed: int = 42):
        """
        Initialiseer de HillClimber met willekeurig gegenereerde routes.

        Args:
            network: Het railnetwerk om mee te werken.
            time_limit: Maximale tijdslimiet voor routes in minuten (default 120).
            max_routes: Maximale aantal routes (default 7).
            seed: Optionele random seed voor reproduceerbaarheid (default 42).
        """
        self.network = network
        self.time_limit = time_limit
        self.max_routes = max_routes
        
        # Houd gebruikte stations globaal bij
        self.used_stations_track = set() 
        
        # Houd gebruikte verbindingen globaal bij
        self.used_connections = set()  

        if seed is not None:
            random.seed(seed)

        self.current_routes = self.generate_random_routes()
        self.update_connection_count()

        print("Gegenereerde Willekeurige Routes:")
        for route in self.current_routes:
            print(route)

    def update_connection_count(self):
        """
        Werk het aantal verbindingen bij op basis van de persistente used_connections_track set.
        """
        self.used_stations_track.clear()
        for route in self.current_routes:
            for i in range(len(route.stations) - 1):
                conn = tuple(sorted((route.stations[i], route.stations[i + 1])))
                self.used_stations_track.add(conn)

        # Sla het aantal unieke gebruikte verbindingen op in het netwerk
        self.network.connections_used = len(self.used_stations_track)

    def generate_random_routes(self) -> List[Route]:
        """
        Genereer een set willekeurige routes, beginnend bij willekeurige stations.

        Return:
            routes: Lijst van gegenereerde routes.
        """
        routes = []
        for _ in range(self.max_routes):
            start_station = random.choice(list(self.network.stations.keys()))
            new_route = self.network.create_route(start_station)

            # Verwijder dubbele stations
            unique_stations = []
            seen_stations = set()
            for station in new_route.stations:
                if station not in seen_stations:
                    unique_stations.append(station)
                    seen_stations.add(station)

            # Werk de route bij met unieke stations
            new_route.stations = unique_stations

            if len(new_route.stations) >= 2:
                routes.append(new_route)

        return routes

    def copy_routes(self, routes: List[Route]) -> List[Route]:
        """
        Maak een diepe kopie van routes om de originele niet te wijzigen.

        Return:
            Lijst van kopieën van de opgegeven routes.
        """
        return deepcopy(routes)

    def modify_route(self, route: Route) -> Route:
        """
        Wijzig een route door een van de volgende strategieën te gebruiken:
        1. Start de route vanaf een willekeurig station.
        2. Vervang de route volledig door een nieuwe willekeurige route.

        Args:
            route: De route die gewijzigd moet worden.

        Return:
            new_route: De gewijzigde route.
        """
        option = random.choice([1, 2])
        
        if option == 1:
            start_station = random.choice(list(self.network.stations.keys()))
            new_route = self.network.create_route(start_station)
        else:
            start_station = random.choice(list(self.network.stations.keys()))
            new_route = self.network.create_route(start_station)

        unique_stations = []
        seen_stations = set()

        for station in new_route.stations:
            if station not in seen_stations:
                unique_stations.append(station)
                seen_stations.add(station)
        new_route.stations = unique_stations
        return new_route

    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Voer de hill-climber uit om de routes voor het netwerk te optimaliseren.

        Args:
            iterations: Het aantal iteraties voor het optimaliseren van de routes (default 1000).

        Return:
            best_quality: De hoogste kwaliteit van de gevonden routes.
            best_routes: Lijst van de beste gevonden routes.
        """
        self.network.routes = self.current_routes
    
        # Bereken de initiële kwaliteit van de huidige routes
        initial_quality = self.network.calculate_quality()
        best_quality = initial_quality
        
        # Maak een kopie van de huidige routes voor het bijhouden van de beste oplossing
        best_routes = self.copy_routes(self.current_routes)
        i = 0
        while i < iterations:
            route = random.choice(self.current_routes)
            route_idx = self.current_routes.index(route)
            old_route = deepcopy(route)
            new_route = self.modify_route(route)
            self.current_routes[route_idx] = new_route
            
            # Werk de verbindingen bij die door de routes gebruikt worden
            self.update_connection_count()
            
            # Werk het netwerk bij met de nieuwe routes
            self.network.routes = self.current_routes

            # Bereken de kwaliteit van de nieuwe routes
            new_quality = self.network.calculate_quality()

            if new_quality > best_quality:
                # Update de beste kwaliteit
                best_quality = new_quality
                best_routes = self.copy_routes(self.current_routes)
            else:
                # Zet de route terug naar de oude
                self.current_routes[route_idx] = old_route
                self.update_connection_count()
            i += 1
        return best_quality, best_routes
