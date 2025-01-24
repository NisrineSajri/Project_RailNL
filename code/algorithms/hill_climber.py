import random
from copy import deepcopy
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route


class HillClimber:
    def __init__(self, network: RailNetwork, time_limit: int = 120, max_routes: int = 7, seed: None | int = 42):
        """
        Initialize the HillClimber with randomly generated routes.

        Args:
            network: The rail network to work with.
            time_limit: Maximum time limit for routes in minutes.
            max_routes: Maximum number of routes.
            used_stations: Track used stations globally
            used_connections_track: Track used connections globally
            seed: Optional random seed for reproducibility.
        """
        self.network = network
        self.time_limit = time_limit
        self.max_routes = max_routes
        
         # Track used stations globally
        self.used_stations_track = set() 
        
        # Track used connections globally
        self.used_connections = set()  

        if seed is not None:
            random.seed(seed)

        self.current_routes = self.generate_random_routes()
        self.update_connection_count()

        print("Generated Random Routes:")
        for route in self.current_routes:
            print(route)

  
    # mijn connecties tellen niet goed, daarom dit 
    def update_connection_count(self):
        """
        Update the connection count based on the persistent `used_connections_track` set.
        """
        # Maak de set van gebruikte stations leeg
        self.used_stations_track.clear()
        for route in self.current_routes:
            # Loop door de stations in de route, stop 1 station voor het laatste
            for i in range(len(route.stations) - 1):
                # Het sorteren zorgt ervoor dat de verbinding tussen station A en B hetzelfde is als tussen B en A
                conn = tuple(sorted((route.stations[i], route.stations[i + 1])))
                
                # Voeg de verbinding toe aan de set van gebruikte verbindingen
                self.used_stations_track.add(conn)

        # Sla het aantal unieke gebruikte verbindingen op in het netwerk
        self.network.connections_used = len(self.used_stations_track)

    def generate_random_routes(self) -> List[Route]:
        """Generate a set of random routes starting from random stations."""
        routes = []
        for _ in range(self.max_routes):
            start_station = random.choice(list(self.network.stations.keys()))
            new_route = self.network.create_route(start_station)

            # Remove duplicate stations
            unique_stations = []
            seen_stations = set()
            for station in new_route.stations:
                if station not in seen_stations:
                    unique_stations.append(station)
                    seen_stations.add(station)

            # Update the route with unique stations
            new_route.stations = unique_stations

            # Ensure route has at least two valid connection
            if len(new_route.stations) >= 2:
                routes.append(new_route)

        return routes

    def copy_routes(self, routes: List[Route]) -> List[Route]:
        """Create a deep copy of routes to avoid modifying the originals."""
        return deepcopy(routes)

    def modify_route(self, route: Route) -> Route:
        """
        Modify a route by using one of the following strategies:
        1. Restart the route from a random station.
        2. Replace the route entirely with a random new one.
        """
        # Choose a strategy randomly
        option = random.choice([1, 2])
        
        if option == 1:
            # Strategy 1: Restart the route from a random station
            start_station = random.choice(list(self.network.stations.keys()))
            new_route = self.network.create_route(start_station)

        else:
            # Strategy 2: Replace the route entirely with a random new one
            start_station = random.choice(list(self.network.stations.keys()))
            new_route = self.network.create_route(start_station)

        # Maak een lege lijst om de unieke stations op te slaan
        unique_stations = []

        # Maak een set om bij te houden welke stations al zijn toegevoegd
        seen_stations = set()

        # Loop door alle stations in de nieuwe route
        for station in new_route.stations:
            # Als het station nog niet in de set 'seen_stations' zit
            if station not in seen_stations:
                unique_stations.append(station)
                seen_stations.add(station)
        new_route.stations = unique_stations
        return new_route


    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Run the hill-climber to optimize routes for the network.
        """
        self.network.routes = self.current_routes
    
        # Bereken de initiële kwaliteit van de huidige routes
        initial_quality = self.network.calculate_quality()
        best_quality = initial_quality
        
        # Maak een kopie van de huidige routes voor het bijhouden van de beste oplossing
        best_routes = self.copy_routes(self.current_routes)
        i = 0
        while i < iterations:
            # Kies willekeurig een route uit de huidige routes
            route = random.choice(self.current_routes)
            
            # Zoek de index van de geselecteerde route in de lijst
            route_idx = self.current_routes.index(route)
            
            # Maak een diepe kopie van de geselecteerde route als het terug moet
            old_route = deepcopy(route)
            new_route = self.modify_route(route)
            
            # Zet de gewijzigde route op de oorspronkelijke plek in de lijst
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