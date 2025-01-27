from typing import List
import csv
import os
import sys
import pandas as pd
import folium
import matplotlib.pyplot as plt

# Voeg de bovenliggende map toe aan het Python-pad
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from classes.route import Route

class SolutionStatistics:
    def __init__(self, quality: float, routes: List[Route], network=None, *args):
        """
        Initialiseer SolutionStatistics met een kwaliteitscore en routes.
        
        Args:
            quality (float): De kwaliteitscore van de oplossing.
            routes (List[Route]): Een lijst van routes in de oplossing.
            network: Het spoorwegnetwerk dat wordt gebruikt.
        """
        self.quality = quality
        self.routes = routes
        self.network = network
        self.total_time = sum(route.total_time for route in routes) if routes else 0
        self.total_connections = sum(len(route.connections_used) for route in routes) if routes else 0
        
    def print_stats(self):
        """
        Print uitgebreide statistieken over de oplossing.
        """
        if not self.routes:
            print("\nNo valid routes found!")
            return
            
        print("\nSolution Statistics:")
        print(f"Quality Score (K): {self.quality:.2f}")
        print(f"Number of routes (T): {len(self.routes)}")
        print(f"Total time (Min): {self.total_time} minutes")
        print(f"Total connections used: {self.total_connections}")
        print(f"Coverage percentage: {self.get_coverage_percentage():.1f}%")

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
        Verkrijg een samenvatting van de oplossing in dictionaryvorm.
        
        Returns:
            dict: Samenvatting van statistieken, inclusief kwaliteit, aantal routes, 
                  totale tijd en aantal verbindingen.
        """
        return {
            'quality': self.quality,
            'num_routes': len(self.routes) if self.routes else 0,
            'total_time': self.total_time,
            'total_connections': self.total_connections
        }
        
    def get_coverage_percentage(self) -> float:
        """
        Bereken het percentage van de totale mogelijke verbindingen dat wordt gebruikt.
        
        Returns:
            float: Percentage van gebruikte verbindingen.
        """
        if not self.routes or not self.routes[0].connections_used or not self.network:
            return 0.0
            
        # Verkrijg alle unieke verbindingen van een route
        used_connections = set()
        for route in self.routes:
            used_connections.update(route.connections_used)
            
        # Verkrijg het totaal aantal mogelijke verbindingen van het netwerk
        total_possible = len(self.network.connections)
        
        return (len(used_connections) / total_possible) * 100 if total_possible > 0 else 0.0
        
    def compare_with(self, other: 'SolutionStatistics') -> dict:
        """
        Vergelijk deze oplossing met een andere oplossing.
        
        Args:
            other (SolutionStatistics): Een andere oplossing om mee te vergelijken.
            
        Returns:
            dict: Verschillen in sleutelstatistieken zoals kwaliteit, aantal routes,
                  totale tijd en aantal verbindingen.
        """
        return {
            'quality_diff': self.quality - other.quality,
            'routes_diff': len(self.routes) - len(other.routes),
            'time_diff': self.total_time - other.total_time,
            'connections_diff': self.total_connections - other.total_connections
        }
    
    def visualisation_algorithms(self):
        """
        Genereer een visualisatie van de routes en sla deze op als een HTML-bestand.
        """
        # Maak een visualisatiemap als deze nog niet bestaat
        os.makedirs('visualization', exist_ok=True)
        
        # Sla de routes van het algoritme dat via main wordt uitgevoerd op in routes.csv
        with open('visualization/routes.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for route in self.routes:
                # We willen geen dubbele stations op één rij
                route_unique = []
                previous_station = None
                for station in route.stations:
                    if station != previous_station:
                        route_unique.append(station)
                    previous_station = station

                # Nu hebben we alle routes zonder dubbele stations
                writer.writerow(route_unique)

        # Maak een dictionary met coördinaten van elk station gekoppeld aan het station
        stations = pd.read_csv('../data/StationsNationaal.csv', header=None, names=['station', 'y', 'x'], skiprows=1)
        station_coordinate = {}
        for index, row in stations.iterrows():
            station = row['station']
            y_coordinate = row['y']
            x_coordinate = row['x']
            station_coordinate[station] = {'y': y_coordinate, 'x': x_coordinate}

        # Creëer een kaart ingezoomd op Nederland
        m = folium.Map(location=[52.1326, 4.2913], zoom_start=7)
        for station, coordinate in station_coordinate.items():
            # Controleer of elk station in een van de routes zit, en plaats een marker
            if any(station in route.stations for route in self.routes):
                folium.Marker(
                    location=[coordinate['y'], coordinate['x']],
                    popup=station,
                ).add_to(m)

        colors = [
            "red", "green", "yellow", "blue", "orange", "purple",
            "cyan", "magenta", "lime", "darkblue", "teal", "gold",
            "pink", "darkred", "violet", "olive", "indigo", "salmon",
            "turquoise", "plum"
        ]

        # Gebruik een kleurindex voor verschillende kleuren
        color_index = 0  

        # Doorloop elke berekende route
        for route in self.routes:
            route_unique = []
            previous_station = None
            for station in route.stations:
                if station != previous_station:
                    route_unique.append(station)
                previous_station = station
            
            route_description = f"Route {color_index + 1}:\n" + " -> ".join(route_unique)

            for i in range(len(route.stations) - 1):
                # Definieer de start- en eindstations uit de lijst met routes
                station1 = route.stations[i]
                station2 = route.stations[i + 1]

                if station1 in station_coordinate and station2 in station_coordinate:
                    # Verbind de start- en eindstations met lijnen
                    folium.PolyLine(
                        locations=[
                            [station_coordinate[station1]['y'], station_coordinate[station1]['x']],
                            [station_coordinate[station2]['y'], station_coordinate[station2]['x']]
                        ],
                        color=colors[color_index],
                        opacity=0.8,
                        weight=5,
                        popup=folium.Popup(route_description, max_width=200)
                    ).add_to(m)
            # Zorg ervoor dat elke route een andere kleur heeft
            color_index += 1
        
        # Sla het bestand op in de visualisatiemap
        m.save("visualization/visualization_algorithms.html")