from typing import List
import csv
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from classes.route import Route

class SolutionStatistics:
    def __init__(self, quality: float, routes: List[Route]):
        """
        Initialize SolutionStatistics with quality score and routes.
        
        Args:
            quality (float): Quality score of the solution
            routes (List[Route]): List of routes in the solution
        """
        self.quality = quality
        self.routes = routes
        self.total_time = sum(route.total_time for route in routes) if routes else 0
        self.total_connections = sum(len(route.connections_used) for route in routes) if routes else 0
        
    def print_stats(self):
        """Print comprehensive statistics about the solution"""
        if not self.routes:
            print("\nNo valid routes found!")
            return
            
        print("\nSolution Statistics:")
        print(f"Quality Score (K): {self.quality:.2f}")
        print(f"Number of routes (T): {len(self.routes)}")
        print(f"Total time (Min): {self.total_time} minutes")
        print(f"Total connections used: {self.total_connections}")

        # Opslaan van de routes in een CSV-bestand
        with open('routes.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for route in self.routes:
                writer.writerow(route.stations)

        print(f"Routes have been saved to 'routes.csv'.")
        
        print("\nDetailed Routes:")
        for i, route in enumerate(self.routes, 1):
            print(f"\nRoute {i}:")
            print(f"Stations: {' -> '.join(route.stations)}")
            print(f"Time: {route.total_time} minutes")
            print(f"Connections: {len(route.connections_used)}")
            
    def get_summary(self) -> dict:
        """
        Get a dictionary containing summary statistics.
        
        Returns:
            dict: Summary statistics including quality, number of routes,
                 total time, and total connections
        """
        return {
            'quality': self.quality,
            'num_routes': len(self.routes) if self.routes else 0,
            'total_time': self.total_time,
            'total_connections': self.total_connections
        }
        
    def get_coverage_percentage(self) -> float:
        """
        Calculate the percentage of total possible connections that are used.
        
        Returns:
            float: Percentage of connections covered
        """
        if not self.routes or not self.routes[0].connections_used:
            return 0.0
            
        # Get all unique connections from any route
        used_connections = set()
        for route in self.routes:
            used_connections.update(route.connections_used)
            
        # Get the first connection to access the rail network
        first_conn = next(iter(used_connections))
        # Count total possible connections in the network
        total_possible = len(first_conn.rail_network.connections)
        
        return (len(used_connections) / total_possible) * 100 if total_possible > 0 else 0.0
        
    def compare_with(self, other: 'SolutionStatistics') -> dict:
        """
        Compare this solution with another solution.
        
        Args:
            other (SolutionStatistics): Another solution to compare with
            
        Returns:
            dict: Dictionary containing differences in key metrics
        """
        return {
            'quality_diff': self.quality - other.quality,
            'routes_diff': len(self.routes) - len(other.routes),
            'time_diff': self.total_time - other.total_time,
            'connections_diff': self.total_connections - other.total_connections
        }