# hill_climber.py
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.station import Station

class HilClimberAlgorithm:




    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Find best solution (single iteration since deterministic).
        
        Args:
            iterations: Kept for API compatibility
            
        Returns:
            Tuple[float, List[Route]]: Quality score and corresponding routes
        """
        quality = self.runGreedy()
        best_routes = [Route() for _ in self.network.routes]
        for new_route, old_route in zip(best_routes, self.network.routes):
            new_route.stations = old_route.stations.copy()
            new_route.total_time = old_route.total_time
            new_route.connections_used = old_route.connections_used.copy()
        
        return quality, best_routes