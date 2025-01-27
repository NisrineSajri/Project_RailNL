from typing import List, Tuple, Optional
import random
from collections import deque
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.heuristics import RouteHeuristics

class HeuristicRandomBFS:
    def __init__(self, rail_network: RailNetwork, time_limit: int = 120, max_routes: int = 7):
        """
        Initialize HeuristicRandomBFS.
        
        Args:
            rail_network: The rail network to work with
            time_limit: Maximum time limit for routes in minutes
            max_routes: Maximum number of routes allowed
        """
        self.rail_network = rail_network
        self.time_limit = time_limit
        self.max_routes = max_routes
        self.heuristic = RouteHeuristics(rail_network, time_limit=time_limit)

    def create_route(self, start_station: str) -> Route:
        """
        Create a single route using heuristic-guided random BFS.
        
        Args:
            start_station: Starting station name
            
        Returns:
            Route: Created route
        """
        route = Route()
        queue = deque([(start_station, [start_station], 0, set([start_station]))])
        best_route = None
        best_score = float('-inf')
        
        while queue:
            current_station, path, total_time, visited = queue.popleft()
            
            # Get possible next moves using heuristics
            station = self.rail_network.stations[current_station]
            possible_moves = []
            
            for dest, connection in station.connections.items():
                if dest in visited:
                    continue
                    
                if total_time + connection.distance > self.time_limit:
                    continue
                
                # Get heuristic score for this move
                score = self.heuristic.calculate_connection_value(
                    connection, current_station, total_time
                )
                
                if score > float('-inf'):
                    possible_moves.append((score, dest, connection))
            
            if possible_moves:
                # Sort by score and take top half of moves
                possible_moves.sort(reverse=True)
                top_moves = possible_moves[:max(1, len(possible_moves) // 2)]
                
                # Add all top moves to queue for BFS exploration
                for score, next_station, connection in top_moves:
                    new_time = total_time + connection.distance
                    new_path = path + [next_station]
                    new_visited = visited | {next_station}
                    
                    # Create temporary route to evaluate this path
                    temp_route = Route()
                    temp_route.stations = new_path
                    temp_route.total_time = new_time
                    # Add all connections in the path
                    for i in range(len(new_path) - 1):
                        station1 = new_path[i]
                        station2 = new_path[i + 1]
                        # Find the connection between these stations
                        conn = self.rail_network.stations[station1].connections[station2]
                        temp_route.connections_used.add(conn)
                    
                    # Score this route
                    route_score = (
                        len(temp_route.connections_used) * 100  # Value of connections
                        - temp_route.total_time  # Time penalty
                        + score * 10  # Heuristic future value
                    )
                    
                    if route_score > best_score:
                        best_score = route_score
                        best_route = temp_route
                    
                    queue.append((next_station, new_path, new_time, new_visited))
        
        return best_route if best_route else route

    def create_solution(self) -> float:
        """
        Create a complete solution with multiple routes.
        
        Returns:
            float: Quality score of the solution
        """
        # Reset all connections
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        # Get stations sorted by number of connections
        stations = list(self.rail_network.stations.keys())
        routes_created = 0
        
        while routes_created < self.max_routes:
            # Try to find stations with unused connections
            stations_with_unused = [
                station for station in stations
                if any(not conn.used 
                      for conn in self.rail_network.stations[station].connections.values())
            ]
            
            if not stations_with_unused:
                break
            
            # Prioritize stations with more unused connections
            stations_with_unused.sort(
                key=lambda s: sum(1 for conn in self.rail_network.stations[s].connections.values() 
                                if not conn.used),
                reverse=True
            )
            
            # Take from top 3 stations randomly to add variety
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
        Find the best solution through multiple attempts.
        
        Args:
            iterations: Number of attempts to make
            
        Returns:
            Tuple[float, List[Route]]: Best quality score and corresponding routes
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