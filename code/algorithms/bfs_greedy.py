# bfs_greedy.py
from collections import deque
from typing import List, Tuple, Optional, Set
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.heuristics import RouteHeuristics

class SimplifiedBFSAlgorithm:
    def __init__(self, rail_network: RailNetwork):
        self.rail_network = rail_network
        self.heuristic = RouteHeuristics(rail_network)
        
    def find_route_bfs(self, start_station: str, time_limit: int = 120) -> Optional[Route]:
        """
        Use BFS with heuristic guidance to find a good route from given station.
        
        Args:
            start_station (str): Starting station name
            time_limit (int): Maximum route time in minutes (default 120)
            
        Returns:
            Optional[Route]: Best route found, or None if no valid route exists
        """
        # Queue stores: (current_station, path_so_far, total_time, visited_stations, route)
        queue = deque([(start_station, [start_station], 0, {start_station}, Route())])
        best_score = float('-inf')
        best_route = None
        
        while queue:
            current_station, path, total_time, visited, current_route = queue.popleft()
            
            # Try to extend current route
            connection, score = self.heuristic.get_best_connection(
                current_station, total_time, visited
            )
            
            if connection:
                next_station = connection.get_other_station(current_station)
                new_time = total_time + connection.distance
                new_visited = visited | {next_station}
                new_path = path + [next_station]
                
                # Create new route with this connection
                new_route = Route()
                new_route.stations = new_path
                new_route.total_time = new_time
                new_route.connections_used = current_route.connections_used | {connection}
                
                # Update best route if this scores better
                route_score = len(new_route.connections_used) * 100 - new_time
                if route_score > best_score:
                    best_score = route_score
                    best_route = new_route
                
                # Add to queue for further exploration if time permits
                if new_time <= time_limit - 10:  # Leave some buffer
                    queue.append((
                        next_station,
                        new_path,
                        new_time,
                        new_visited,
                        new_route
                    ))
        
        return best_route

    def create_solution(self, max_routes: int = 7) -> float:
        """
        Create a complete solution with multiple routes.
        
        Args:
            max_routes (int): Maximum number of routes allowed
            
        Returns:
            float: Quality score of the solution
        """
        # Reset all connections
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        routes_created = 0
        all_stations = list(self.rail_network.stations.keys())
        
        while routes_created < max_routes:
            best_route = None
            best_station = None
            best_score = float('-inf')
            
            # Try each possible starting station
            for start_station in all_stations:
                route = self.find_route_bfs(start_station)
                if route:
                    # Score based on connections and time
                    score = len(route.connections_used) * 100 - route.total_time
                    if score > best_score:
                        best_score = score
                        best_route = route
                        best_station = start_station
            
            if not best_route:
                break
                
            # Add the best route found to our solution
            for conn in best_route.connections_used:
                conn.used = True
            self.rail_network.routes.append(best_route)
            routes_created += 1
            
            # Remove used starting station from consideration
            if best_station in all_stations:
                all_stations.remove(best_station)
        
        return self.rail_network.calculate_quality()

    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Find the best solution. Single iteration since deterministic.
        
        Args:
            iterations (int): Kept for API compatibility
            
        Returns:
            Tuple[float, List[Route]]: Quality score and routes
        """
        quality = self.create_solution()
        best_routes = [Route() for _ in self.rail_network.routes]
        for new_route, old_route in zip(best_routes, self.rail_network.routes):
            new_route.stations = old_route.stations.copy()
            new_route.total_time = old_route.total_time
            new_route.connections_used = old_route.connections_used.copy()
        
        return quality, best_routes