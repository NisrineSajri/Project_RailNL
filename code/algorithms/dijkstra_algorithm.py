# Bronen: 
# https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
# https://stackoverflow.com/questions/69580769/redundant-checks-in-python-implementation-of-dijkstras-algorithm

import csv
import os
import sys
from heapq import heapify, heappop, heappush
import pandas as pd

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

<<<<<<< HEAD
from classes.rail_network import RailNetwork
from classes.route import Route
=======
from constants import HOLLAND_CONFIG
>>>>>>> 728c46670ad81a4541382dcdf7e4f20c4c027fda

# We halen hier de data op van de coördinaten en de verbindingen van de stations
stations = pd.read_csv(HOLLAND_CONFIG['stations_file'], header=None, names=['station', 'y', 'x'], skiprows=1)
connections = pd.read_csv(HOLLAND_CONFIG['connections_file'], header=None, names=['station1', 'station2', 'distance'], skiprows=1)

class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph

    def add_edge(self, node1, node2, weight):
        """Voegt een edge toe tussen twee nodes (beide kanten op) met een weight"""

        # als node1 nog niet bestaat, creëren we deze
        if node1 not in self.graph:
            self.graph[node1] = {}
        # we creëren een verbinding tussen node1 en node2 met een weight
        self.graph[node1][node2] = weight

        # als node2 nog niet bestaat, creëren we deze
        if node2 not in self.graph:
           self.graph[node2] = {}
        # we creëren een verbinding tussen node2 en node1 met een weight
        self.graph[node2][node1] = weight

    def add_connections(self,connections):
        """We creëren een graaf met voor elke verbinding een edge"""
        for _, row in connections.iterrows():
            self.add_edge(row['station1'], row['station2'], row['distance'])

    def shortest_distances(self, source):
        """We zoeken naar de kortste afstand van de source naar andere nodes
            deze functie creërt een dictionary met de kortste afstanden naar alle andere
            stations vanaf de source"""
        # we zetten de distances van alle nodes op oneindig
        distances = {node: float("inf") for node in self.graph}

        # we stellen de afstand naar source gelijk aan 0
        distances[source] = 0

        # We maken een priority queue aan
        pq = [(0, source)]

        # we zetten het om in een queue object
        heapify(pq)

        # zolang de priority queue niet leeg is
        while len(pq) > 0:
           
            # we halen de node op met kortste afstand, dit wordt current_node (current_distance hoort hierbij)
            current_distance, current_node = heappop(pq)

            # als de afstand langer is dan de kortste afstand, gaan we door
            if current_distance > distances[current_node]:
                continue

            # we gaan alle buren van current_node af
            for neighbor, weight in self.graph[current_node].items():
                
                # we berekenen de totale afstand naar neighbor
                distance = current_distance + weight
                
                # als de afstand nu korter is, vervangen we de afstand
                if distance < distances[neighbor]:
                    distances[neighbor] = distance

                    # we voegen de afstand toe aan de priority que
                    heappush(pq, (distance, neighbor))

        # we returnen de dictionary met de distances erin
        #print(source)
        #print(distances)
        return distances

class DijkstraAlgorithm:
    def __init__(self, graph, max_minutes = 120, max_trajects = 7):
        self.graph = graph
        self.max_minutes = max_minutes
        self.max_trajects = max_trajects
        self.railnetwork = RailNetwork()
    
    def calculate_start_station(self, start_stations, visited):
        """We zoeken een startstation dat nog niet bezocht is"""
        for _, row in connections.iterrows():
            if row['station1'] not in start_stations and row['station1'] not in visited:
                start_stations.add(row['station1'])
                return(row['station1'])
            
    def find_next_station(self, start_station, visited, visited_connections):
        """We zoeken het volgende station (met de kortste afstand)"""
        # we vragen de dicitonary op met de kortste afstanden naar andere stations vanaf source
        distances = self.graph.shortest_distances(start_station)
        next_station = None

        # we zetten shortest_distance gelijk aan oneindig

        shortest_distance = float("inf")

        # we gaan alle andere stations af
        for station, distance in distances.items():

            # We kiezen alleen stations waar we nog niet geweest zijn (en niet naar zichzelf)
            if station not in visited and station != start_station:

                # we maken een frozenset (niet veranderbaar) van de connectie tussen start_station en station
                connection = frozenset([start_station, station])

                # als de connectie nog niet is geweest én de distance is korter dan shortest_distance
                if connection not in visited_connections and distance < shortest_distance:
                    next_station = station
                    shortest_distance = distance
        return next_station, shortest_distance

    def traject(self, start_stations, visited_connections):
        """We verwerken één traject"""
        current_traject = []
        current_minutes = 0

        # we maken een set aan om de bezochte plekken in op te slaan

        visited = set()

        start_station = self.calculate_start_station(start_stations, visited)

        while current_minutes < self.max_minutes:
            next_station, shortest_distance = self.find_next_station(start_station, visited, visited_connections)

            if next_station is None or current_minutes + shortest_distance > self.max_minutes:
                break

            # we voegen dit station toe aan de visited set
            visited.add(next_station)

            # we voegen deze verbinding toe aan het huidige trajet
            current_traject.append((start_station, next_station, shortest_distance))

            # we slaan deze connectie toe in de bezochte connecties van alles
            visited_connections.add(frozenset([start_station, next_station]))

            # we updaten de current_minutes
            current_minutes = current_minutes + shortest_distance

            # het nieuwe start station is die van de verbinding
            start_station = next_station

        return current_traject, current_minutes, visited_connections


    def k_value(self, trajects, visited_connections):
        """We berekenen de K"""
        total_connections = len(connections)
        p = len(visited_connections) / total_connections
        T = len(trajects)
        total_minutes = sum(minutes for _, minutes in trajects)
        K = p * 1000 - (T * 100 - total_minutes)
        return K

  
    def find_best_solution(self):
        """We berekenen de routes, deze functie returned de trajecten en de waarde van K"""
        
        # hier slaan we de trajecten op
        trajects = []

        # we houden de bezochte connecties bij
        visited_connections = set()

        # we maken een lege set om de stations in op te slaan die al als startstation gebruikt zijn
        start_stations = set()

        # zolang we 120 minuten niet overschreiden
        while len(trajects) < self.max_trajects:

            current_traject, current_minutes, new_connections = self.traject(start_stations, visited_connections)
            trajects.append((current_traject, current_minutes))
        
        K = self.k_value(trajects, visited_connections)
        return K, trajects

if __name__ == "__main__":
    graph = Graph()
    graph.add_connections(connections)
    algorithm = DijkstraAlgorithm(graph)
    K, routes = algorithm.find_best_solution()


    # resultaten
    connections_visualization = {}
    for i, (traject, minutes) in enumerate(routes):
        print(f"Traject {i + 1} ({minutes} minuten):")
        for start, end, distance in traject:
            print(F"{start} -> {end} ({distance} minuten)")
            connections_visualization[start] = end
    print(f"Kwaliteit K: {K}")
    #print(f"connections dict: {connections_visualization}")

