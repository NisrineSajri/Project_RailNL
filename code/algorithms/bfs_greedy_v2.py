from collections import deque
from typing import List, Tuple, Optional
from classes.rail_network import RailNetwork
from classes.route import Route

class SimplifiedBFSAlgorithm:
    def __init__(self, rail_network: RailNetwork, time_limit: int = 120, max_routes: int = 7):
        """
        Initialize SimplifiedBFSAlgorithm.
        
        Args:
            rail_network: The rail network to work with
            time_limit: Maximum time limit for routes in minutes
            max_routes: Maximum number of routes allowed
        """
        self.rail_network = rail_network
        self.time_limit = time_limit
        self.max_routes = max_routes
        
    def find_route_bfs(self, start_station: str) -> Optional[Route]:
        """
        Use BFS to find a route starting from given station that maximizes unused connections.
        
        Args:
            start_station: Starting station name
            
        Returns:
            Optional[Route]: Best route found, or None if no valid route exists
        """
        # Queue stores: (current_station, path_so_far, total_time, connections_used)
        queue = deque([(start_station, [], 0, set())])
        best_route = None
        best_unused_connections = 0
        
        while queue:
            current_station, path, total_time, connections_used = queue.popleft()
            
            # Get all possible next connections from current station
            station = self.rail_network.stations[current_station]
            possible_connections = [
                (dest, conn) for dest, conn in station.connections.items()
                if total_time + conn.distance <= self.time_limit
            ]
            
            # Try each possible next connection
            for next_station, connection in possible_connections:
                new_time = total_time + connection.distance
                new_path = path + [current_station]
                new_connections = connections_used | {connection}
                
                # Count how many unused connections this route would use
                unused_connections = sum(1 for conn in new_connections if not conn.used)
                
                # Update best route if this one uses more unused connections
                if unused_connections > best_unused_connections:
                    best_unused_connections = unused_connections
                    best_route = Route()
                    best_route.stations = new_path + [next_station]
                    best_route.total_time = new_time
                    best_route.connections_used = new_connections
                
                # Add this state to queue for further exploration
                queue.append((next_station, new_path, new_time, new_connections))
        
        return best_route

    def create_solution(self, max_routes: int = None) -> float:
        """
        Create a complete solution with multiple routes.
        
        Args:
            max_routes: Maximum number of routes allowed
            
        Returns:
            float: Quality score of the solution
        """
        # Use instance default if not specified
        max_routes = max_routes or self.max_routes
        
        # Reset all connections
        for conn in self.rail_network.connections:
            conn.used = False
        self.rail_network.routes.clear()
        
        routes_created = 0
        all_stations = list(self.rail_network.stations.keys())
        
        while routes_created < max_routes:
            best_route = None
            best_station = None
            
            # Try each possible starting station
            for start_station in all_stations:
                route = self.find_route_bfs(start_station)
                if route and (not best_route or 
                            len(route.connections_used) > len(best_route.connections_used)):
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
            iterations: Kept for API compatibility
            
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