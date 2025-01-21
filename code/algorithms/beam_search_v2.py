from typing import List, Tuple, Optional, Set
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.heuristics import RouteHeuristics
import heapq
import random

class BeamSearchAlgorithmV2:
    def __init__(self, rail_network: RailNetwork, beam_width: int = 7, time_limit: int = 120, max_routes: int = 7):
        """
        Initialize BeamSearchAlgorithm with improved heuristics.
        
        Args:
            rail_network: The rail network to work with
            beam_width: Number of best partial solutions to keep at each step
            time_limit: Maximum time limit for routes in minutes
        """
        self.rail_network = rail_network
        self.beam_width = beam_width
        self.time_limit = time_limit
        self.heuristic = RouteHeuristics(rail_network, time_limit=time_limit)
        self.max_routes = max_routes
        
    def find_route_beam(self, start_station: str) -> Optional[Route]:
        """
        Use beam search with improved heuristics and diversity to find a route.
        
        Args:
            start_station: Starting station name
            
        Returns:
            Optional[Route]: Best route found, or None if no valid route exists
        """
        initial_route = Route()
        initial_route.stations = [start_station]
        # Add small random factor to initial state for diversity
        beam = [(random.uniform(0, 0.1), start_station, [start_station], 0, {start_station}, initial_route)]
        best_route = None
        best_score = float('-inf')
        
        while beam:
            new_beam = []
            
            for _, current_station, path, total_time, visited, current_route in beam:
                station = self.rail_network.stations[current_station]
                
                # Get all valid next connections with their scores
                next_moves = []
                # Randomize connection order
                connections = list(station.connections.items())
                random.shuffle(connections)
                
                for dest, connection in connections:
                    if dest in visited:
                        continue
                        
                    new_time = total_time + connection.distance
                    if new_time > self.time_limit:
                        continue
                    
                    # Use heuristic with added randomness
                    base_score = self.heuristic.calculate_connection_value(
                        connection, current_station, total_time
                    )
                    diversity_score = random.uniform(0.95, 1.05)  # Add 5% randomness
                    score = base_score * diversity_score
                    next_moves.append((score, dest, connection))
                
                # Take top K moves based on scores
                next_moves.sort(reverse=True)  # Sort by score
                for score, dest, connection in next_moves[:self.beam_width]:
                    new_time = total_time + connection.distance
                    
                    # Create new route with this connection
                    new_route = Route()
                    new_route.stations = path + [dest]
                    new_route.total_time = new_time
                    new_route.connections_used = current_route.connections_used | {connection}
                    
                    # Enhanced scoring with multiple factors
                    route_score = (
                        len(new_route.connections_used) * 100  # Connection value
                        - new_route.total_time  # Time penalty
                        + score * 10  # Heuristic value
                        # Add bonus for nearby unused connections
                        + sum(1 for conn in self.rail_network.connections 
                            if not conn.used and dest in [conn.station1, conn.station2]) * 5
                    )
                    
                    # Update best complete route if applicable
                    if route_score > best_score:
                        best_score = route_score
                        best_route = new_route
                    
                    # Add to candidates for new beam with small random factor
                    priority = -route_score + random.uniform(0, 0.1)
                    new_beam.append((
                        priority,  # Priority with small random factor
                        dest,
                        path + [dest],
                        new_time,
                        visited | {dest},
                        new_route
                    ))
            
            # Keep only the best beam_width candidates
            beam = heapq.nsmallest(self.beam_width, new_beam)
            
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
            best_score = float('-inf')
            
            # Shuffle stations for more diversity
            random.shuffle(all_stations)
            
            # Try each possible starting station
            for start_station in all_stations:
                route = self.find_route_beam(start_station)
                if route:
                    # Enhanced scoring for route selection
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
                        + random.uniform(-1, 1)  # Small random factor
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