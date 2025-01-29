from typing import List, Tuple, Optional, Set
from classes.rail_network import RailNetwork
from classes.route import Route
import heapq

class BeamSearchAlgorithm:
    def __init__(self, rail_network: RailNetwork, beam_width: int = 6, time_limit: int = 120, max_routes: int = 7):
        """
        Initialiseer BeamSearchAlgorithm.
        
        Args:
            rail_network: Het spoornetwerk om mee te werken
            beam_width: Aantal beste deeloplossingen om te behouden in elke stap
            time_limit: Maximale tijdslimiet voor routes in minuten
            max_routes: Maximaal toegestane aantal routes
        """
        self.rail_network = rail_network
        self.beam_width = beam_width
        self.time_limit = time_limit
        self.max_routes = max_routes
        
    def score_partial_route(self, route: Route) -> float:
        """
        Bereken een score voor een gedeeltelijke route op basis van ongebruikte verbindingen.
        
        Args:
            route: Route om te scoren
            
        Returns:
            float: Score gebaseerd op ongebruikte verbindingen en tijdsefficiëntie
        """
        # Basisscore van ongebruikte verbindingen
        connection_value = len(route.connections_used) * 100
        time_penalty = route.total_time
        
        # Voeg waarde toe voor nabijgelegen ongebruikte verbindingen
        unused_nearby = sum(
            1 for conn in self.rail_network.connections 
            if not conn.used and any(
                station in route.stations 
                for station in [conn.station1, conn.station2]
            )
        )
        
        return connection_value - time_penalty + unused_nearby * 10

    def find_route_beam(self, start_station: str) -> Optional[Route]:
        """
        Gebruik beam search om een route te vinden vanaf het gegeven station.
        
        Args:
            start_station: Naam van het startstation
            
        Returns:
            Optional[Route]: Beste gevonden route, of None als er geen geldige route bestaat
        """
        initial_route = Route()
        initial_route.stations = [start_station]
        beam = [(0, start_station, [start_station], 0, {start_station}, initial_route)]
        best_route = None
        best_score = float('-inf')
        
        while beam:
            new_beam = []
            
            for _, current_station, path, total_time, visited, current_route in beam:
                station = self.rail_network.stations[current_station]
                
                # Verzamel alle mogelijke volgende verbindingen
                for dest, connection in station.connections.items():
                    if dest in visited:
                        continue
                        
                    new_time = total_time + connection.distance
                    if new_time > self.time_limit:
                        continue
                    
                    new_route = Route()
                    new_route.stations = path + [dest]
                    new_route.total_time = new_time
                    new_route.connections_used = current_route.connections_used | {connection}
                    
                    # Score alleen gebaseerd op ongebruikte verbindingen en tijd
                    score = self.score_partial_route(new_route)
                    
                    if score > best_score:
                        best_score = score
                        best_route = new_route
                    
                    new_beam.append((
                        -score,  # Negatief voor min-heap
                        dest,
                        path + [dest],
                        new_time,
                        visited | {dest},
                        new_route
                    ))
            
            # Behoud alleen de beste beam_width kandidaten
            beam = heapq.nsmallest(self.beam_width, new_beam)
        
        return best_route

    def create_solution(self, max_routes: int = None) -> float:
        """
        Maak een complete oplossing met meerdere routes.
        
        Args:
            max_routes: Maximaal toegestane aantal routes
            
        Returns:
            float: Kwaliteitsscore van de oplossing
        """
        # Gebruik standaardwaarde indien niet gespecificeerd
        max_routes = max_routes or self.max_routes
        
        # Reset alle verbindingen
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        routes_created = 0
        all_stations = list(self.rail_network.stations.keys())
        
        # Sorteer stations op aantal ongebruikte verbindingen
        while routes_created < max_routes:
            # Verkrijg stations gesorteerd op aantal ongebruikte verbindingen
            stations_by_connections = sorted(
                all_stations,
                key=lambda s: sum(1 for conn in self.rail_network.stations[s].connections.values() 
                                if not conn.used),
                reverse=True
            )
            
            best_route = None
            best_station = None
            best_score = float('-inf')
            
            # Probeer elk station in volgorde van ongebruikte verbindingen
            for start_station in stations_by_connections:
                route = self.find_route_beam(start_station)
                if route:
                    score = len(route.connections_used) * 100 - route.total_time
                    if score > best_score:
                        best_score = score
                        best_route = route
                        best_station = start_station
            
            if not best_route:
                break
                
            # Voeg de beste gevonden route toe aan onze oplossing
            for conn in best_route.connections_used:
                conn.used = True
            self.rail_network.routes.append(best_route)
            routes_created += 1
            
            if best_station in all_stations:
                all_stations.remove(best_station)
        
        return self.rail_network.calculate_quality()

    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Vind de beste oplossing door verschillende beam breedtes te proberen.
        
        Args:
            iterations: Aantal beam breedtes om te proberen
            
        Returns:
            Tuple[float, List[Route]]: Beste kwaliteitsscore en bijbehorende routes
        """
        best_quality = float('-inf')
        best_routes = []
        
        # Probeer verschillende beam breedtes
        min_beam = 2
        max_beam = min(iterations + 2, len(self.rail_network.stations) // 2)
        
        for beam_width in range(min_beam, max_beam + 1):
            self.beam_width = beam_width
            quality = self.create_solution()
            
            if quality > best_quality:
                best_quality = quality
                best_routes = [Route() for _ in self.rail_network.routes]
                for new_route, old_route in zip(best_routes, self.rail_network.routes):
                    new_route.stations = old_route.stations.copy()
                    new_route.total_time = old_route.total_time
                    new_route.connections_used = old_route.connections_used.copy()
        
        return best_quality, best_routes