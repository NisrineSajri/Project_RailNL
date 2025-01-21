from typing import List, Tuple, Optional, Set
from classes.rail_network import RailNetwork
from classes.route import Route
import random
import heapq

class BeamSearchAlgorithm:
    def __init__(self, rail_network: RailNetwork, beam_width: int = 6, time_limit: int = 120, max_routes: int = 7):
        """
        Initialize BeamSearchAlgorithm.
        
        Args:
            rail_network: The rail network to work with
            beam_width: Number of best partial solutions to keep at each step
            time_limit: Maximum time limit for routes in minutes
        """
        self.rail_network = rail_network
        self.beam_width = beam_width
        self.time_limit = time_limit
        self.max_routes = max_routes
        
    def score_partial_route(self, route: Route) -> float:
        """
        Score a partial route with improved heuristics.
        """
        # Base score from connections and time
        connection_value = len(route.connections_used) * 100
        time_penalty = route.total_time
        
        # Add diversity factor based on unused connections nearby
        unused_nearby = sum(
            1 for conn in self.rail_network.connections 
            if not conn.used and any(
                station in route.stations 
                for station in [conn.station1, conn.station2]
            )
        )
        
        # Randomization factor to break ties and increase diversity
        random_factor = random.uniform(0.95, 1.05)
        
        return (connection_value - time_penalty + unused_nearby * 10) * random_factor

    def find_route_beam(self, start_station: str) -> Optional[Route]:
        """
        Use beam search to find a route with improved diversity.
        """
        initial_route = Route()
        initial_route.stations = [start_station]
        # Add random tiebreaker to initial state
        beam = [(random.uniform(0, 0.1), start_station, [start_station], 0, {start_station}, initial_route)]
        best_route = None
        best_score = float('-inf')
        
        while beam:
            new_beam = []
            
            for _, current_station, path, total_time, visited, current_route in beam:
                station = self.rail_network.stations[current_station]
                
                # Shuffle connections to increase diversity
                connections = list(station.connections.items())
                random.shuffle(connections)
                
                for dest, connection in connections:
                    if dest in visited:
                        continue
                        
                    new_time = total_time + connection.distance
                    if new_time > self.time_limit:
                        continue
                    
                    new_route = Route()
                    new_route.stations = path + [dest]
                    new_route.total_time = new_time
                    new_route.connections_used = current_route.connections_used | {connection}
                    
                    # Score with randomization factor
                    score = self.score_partial_route(new_route)
                    
                    if score > best_score:
                        best_score = score
                        best_route = new_route
                    
                    new_beam.append((
                        -score,  # Priority
                        dest,
                        path + [dest],
                        new_time,
                        visited | {dest},
                        new_route
                    ))
            
            # Add random tiebreaker to beam selection
            beam = []
            for item in heapq.nsmallest(self.beam_width, new_beam):
                priority = item[0] + random.uniform(0, 0.1)  # Small random factor
                beam.append((priority,) + item[1:])
        
        return best_route

    def create_solution(self, max_routes: int = None) -> float:
        # Use instance default if not specified
        max_routes = max_routes or self.max_routes
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
        
        # Try different beam widths
        for beam_width in range(2, iterations + 2):
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