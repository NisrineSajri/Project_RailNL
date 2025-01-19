from typing import List
import csv
import os
import sys
import pandas as pd
import folium

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

        print("\nDetailed Routes:")
        for i, route in enumerate(self.routes, 1):
            print(f"\nRoute {i}:")
            print(f"Stations: {' -> '.join(route.stations)}")
            print(f"Time: {route.total_time} minutes")
            print(f"Connections: {len(route.connections_used)}")

        self.visualisation_algorithms()
        print("For the visualization of the routes go to visualization_algorithms.html")
        
            
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
    
    def visualisation_algorithms(self):
        # Bron: https://www.tutorialspoint.com/how-to-save-a-python-dictionary-to-csv-file
        # We slaan de routes van het algoritme dat we runnen via main op in routes.csv
        with open('visualization/routes.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for route in self.routes:

                # we willen geen dubbele stations op één rij
                route_unique = []
                previous_station = None
                for station in route.stations:
                    if station != previous_station:
                        route_unique.append(station)
                    previous_station = station

                # we hebben nu alle routes zonder dubbele stations
                writer.writerow(route_unique)

        # We maken een dictionary met de coördinaten van elk station gekoppeld aan het bijbehorende station
        stations = pd.read_csv('../data/StationsNationaal.csv', header=None, names=['station', 'y', 'x'], skiprows=1)
        station_coordinate = {}
        for index, row in stations.iterrows():
            station = row['station']
            y_coordinate = row['y']
            x_coordinate = row['x']
            station_coordinate[station] = {'y': y_coordinate, 'x': x_coordinate}

        # We creëren een kaart gezoomed op Nederland
        m = folium.Map(location=[52.1326, 4.2913], zoom_start=7)

        for station, coordinate in station_coordinate.items():
            # We kijken elk station in één van de routes zit, en plaatsen hier een marker
            if any(station in route.stations for route in self.routes):
                folium.Marker(
                    location=[coordinate['y'], coordinate['x']],
                    popup=station,
                ).add_to(m)

        # Bron: https://gist.github.com/blaylockbk/0f95f9e57f7713a890ebf01be088dc5e
        colors = [
            "red",
            "green",
            "yellow",
            "blue",
            "orange",
            "purple",
            "cyan",
            "magenta",
            "lime",
            "pink",
            "teal",
            "lavender",
            "brown",
            "beige",
            "maroon",
            "mint",
            "olive",
            "apricot",
            "navy",
            "grey",
        ]

        # We gebruiken een color index voor de verschillende kleuren
        color_index = 0  

        # We gaan elke berekende route door
        for route in self.routes:
            for i in range(len(route.stations) - 1):
                # We definiëren de start en eind-stations uit de lijst met routes
                station1 = route.stations[i]
                station2 = route.stations[i + 1]

                if station1 in station_coordinate and station2 in station_coordinate:
                # We verbinden de start en eind-stations met elkaar met lijnen
                    folium.PolyLine(
                        locations=[
                            [station_coordinate[station1]['y'], station_coordinate[station1]['x']],
                            [station_coordinate[station2]['y'], station_coordinate[station2]['x']]
                        ], color = colors[color_index]
                    ).add_to(m)
            # Zodat elke route een andere kleur heeyt
            color_index = color_index + 1
        
        # We slaan het bestand op in de visualization map
        m.save("visualization/visualization_algorithms.html")



        

