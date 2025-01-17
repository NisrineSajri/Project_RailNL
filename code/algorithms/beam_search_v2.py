# beam_search_v2.py
from typing import List, Tuple, Optional, Set
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.heuristics import RouteHeuristics
import heapq

class BeamSearchAlgorithmV2:
    def __init__(self, rail_network: RailNetwork, beam_width: int = 5):
        """
        Initialize BeamSearchAlgorithm with improved heuristics.
        
        Args:
            rail_network: The rail network to work with
            beam_width: Number of best partial solutions to keep at each step
        """
        self.rail_network = rail_network
        self.beam_width = beam_width
        self.heuristic = RouteHeuristics(rail_network)
        
    def find_route_beam(self, start_station: str, time_limit: int = 120) -> Optional[Route]:
        """
        Use beam search with improved heuristics to find a route.
        
        Args:
            start_station: Starting station name
            time_limit: Maximum route time in minutes
            
        Returns:
            Optional[Route]: Best route found, or None if no valid route exists
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
                
                # Get all valid next connections with their scores
                next_moves = []
                for dest, connection in station.connections.items():
                    if dest in visited:
                        continue
                        
                    new_time = total_time + connection.distance
                    if new_time > time_limit:
                        continue
                    
                    # Use heuristic to score this move
                    score = self.heuristic.calculate_connection_value(
                        connection, current_station, total_time
                    )
                    next_moves.append((score, dest, connection))
                
                # Take top K moves based on heuristic
                next_moves.sort(reverse=True)  # Sort by score
                for score, dest, connection in next_moves[:self.beam_width]:
                    new_time = total_time + connection.distance
                    
                    # Create new route with this connection
                    new_route = Route()
                    new_route.stations = path + [dest]
                    new_route.total_time = new_time
                    new_route.connections_used = current_route.connections_used | {connection}
                    
                    # Score includes both heuristic and actual value
                    route_score = (
                        len(new_route.connections_used) * 100  # Value of connections
                        - new_route.total_time  # Time penalty
                        + score * 10  # Heuristic future value
                    )
                    
                    # Update best complete route if applicable
                    if route_score > best_score:
                        best_score = route_score
                        best_route = new_route
                    
                    # Add to candidates for new beam
                    new_beam.append((
                        -route_score,  # Priority (negative for min-heap)
                        dest,
                        path + [dest],
                        new_time,
                        visited | {dest},
                        new_route
                    ))
            
            # Keep only the best beam_width candidates
            beam = heapq.nsmallest(self.beam_width, new_beam)
            
        return best_route

    def create_solution(self, max_routes: int = 7) -> float:
        """
        Create a complete solution with multiple routes.
        
        Args:
            max_routes: Maximum number of routes allowed
            
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
                route = self.find_route_beam(start_station)
                if route:
                    # Score based on connections, time, and remaining potential
                    unused_nearby = sum(
                        1 for conn in self.rail_network.connections 
                        if not conn.used and any(
                            station in route.stations 
                            for station in [conn.station1, conn.station2]
                        )
                    )
                    score = (
                        len(route.connections_used) * 100  # Connection value
                        - route.total_time  # Time penalty
                        + unused_nearby * 10  # Future potential
                    )
                    
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
            
            if best_station in all_stations:
                all_stations.remove(best_station)
        
        return self.rail_network.calculate_quality()
        
    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Find the best solution by trying different beam widths.
        
        Args:
            iterations: Number of different beam widths to try
            
        Returns:
            Tuple[float, List[Route]]: Best quality score and corresponding routes
        """
        best_quality = float('-inf')
        best_routes = []
        
        # Try different beam widths, but with smarter range based on network size
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