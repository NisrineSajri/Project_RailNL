from typing import List, Tuple, Optional
import random
from collections import deque
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.heuristics import RouteHeuristics

class BeamSearchAlgorithmV3:
    def __init__(self, rail_network: RailNetwork, time_limit: int = 120, max_routes: int = 7):
        """
        Initialiseer HeuristicRandomBFS.
        
        Args:
            rail_network: Het spoornetwerk om mee te werken
            time_limit: Maximale tijdslimiet voor routes in minuten
            max_routes: Maximaal toegestane aantal routes
        """
        self.rail_network = rail_network
        self.time_limit = time_limit
        self.max_routes = max_routes
        self.heuristic = RouteHeuristics(rail_network, time_limit=time_limit)

    def create_route(self, start_station: str) -> Route:
        """
        Maak een enkele route met behulp van heuristisch gestuurde willekeurige BFS.
        
        Args:
            start_station: Naam van het startstation
            
        Returns:
            Route: Gecreëerde route
        """
        route = Route()
        queue = deque([(start_station, [start_station], 0, set([start_station]))])
        best_route = None
        best_score = float('-inf')
        
        while queue:
            current_station, path, total_time, visited = queue.popleft()
            
            # Verzamel mogelijke volgende zetten met behulp van heuristieken
            station = self.rail_network.stations[current_station]
            possible_moves = []
            
            for dest, connection in station.connections.items():
                if dest in visited:
                    continue
                    
                if total_time + connection.distance > self.time_limit:
                    continue
                
                # Verkrijg heuristische score voor deze zet
                score = self.heuristic.calculate_connection_value(
                    connection, current_station, total_time
                )
                
                if score > float('-inf'):
                    possible_moves.append((score, dest, connection))
            
            if possible_moves:
                # Sorteer op score en neem beste helft van zetten
                possible_moves.sort(reverse=True)
                top_moves = possible_moves[:max(1, len(possible_moves) // 2)]
                
                # Voeg alle beste zetten toe aan wachtrij voor BFS verkenning
                for score, next_station, connection in top_moves:
                    new_time = total_time + connection.distance
                    new_path = path + [next_station]
                    new_visited = visited | {next_station}
                    
                    # Maak tijdelijke route om dit pad te evalueren
                    temp_route = Route()
                    temp_route.stations = new_path
                    temp_route.total_time = new_time
                    # Voeg alle verbindingen in het pad toe
                    for i in range(len(new_path) - 1):
                        station1 = new_path[i]
                        station2 = new_path[i + 1]
                        # Zoek de verbinding tussen deze stations
                        conn = self.rail_network.stations[station1].connections[station2]
                        temp_route.connections_used.add(conn)
                    
                    # Score deze route
                    route_score = (
                        len(temp_route.connections_used) * 100  # Waarde van verbindingen
                        - temp_route.total_time  # Tijdstraf
                        + score * 10  # Heuristische toekomstige waarde
                    )
                    
                    if route_score > best_score:
                        best_score = route_score
                        best_route = temp_route
                    
                    queue.append((next_station, new_path, new_time, new_visited))
        
        return best_route if best_route else route

    def create_solution(self) -> float:
        """
        Maak een complete oplossing met meerdere routes.
        
        Returns:
            float: Kwaliteitsscore van de oplossing
        """
        # Reset alle verbindingen
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        # Verkrijg stations gesorteerd op aantal verbindingen
        stations = list(self.rail_network.stations.keys())
        routes_created = 0
        
        while routes_created < self.max_routes:
            # Probeer stations te vinden met ongebruikte verbindingen
            stations_with_unused = [
                station for station in stations
                if any(not conn.used 
                      for conn in self.rail_network.stations[station].connections.values())
            ]
            
            if not stations_with_unused:
                break
            
            # Prioriteer stations met meer ongebruikte verbindingen
            stations_with_unused.sort(
                key=lambda s: sum(1 for conn in self.rail_network.stations[s].connections.values() 
                                if not conn.used),
                reverse=True
            )
            
            # Neem willekeurig één van de top 3 stations voor variatie
            start_station = random.choice(stations_with_unused[:min(3, len(stations_with_unused))])
            route = self.create_route(start_station)
            
            if route and route.connections_used:
                for conn in route.connections_used:
                    conn.used = True
                self.rail_network.routes.append(route)
                routes_created += 1
        
        return self.rail_network.calculate_quality()

    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Vind de beste oplossing door meerdere pogingen.
        
        Args:
            iterations: Aantal te maken pogingen
            
        Returns:
            Tuple[float, List[Route]]: Beste kwaliteitsscore en bijbehorende routes
        """
        best_quality = float('-inf')
        best_routes = []
        
        for i in range(iterations):
            quality = self.create_solution()
            
            if quality > best_quality:
                best_quality = quality
                best_routes = [Route() for _ in self.rail_network.routes]
                for new_route, old_route in zip(best_routes, self.rail_network.routes):
                    new_route.stations = old_route.stations.copy()
                    new_route.total_time = old_route.total_time
                    new_route.connections_used = old_route.connections_used.copy()
        
        return best_quality, best_routes