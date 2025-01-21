# dijkstra_algorithm.py
import csv
import os
import sys
from heapq import heapify, heappop, heappush
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route

class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph

    def add_edge(self, node1, node2, weight):
        """Voegt een edge toe tussen twee nodes (beide kanten op) met een weight"""
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = weight

        if node2 not in self.graph:
           self.graph[node2] = {}
        self.graph[node2][node1] = weight

    def add_connections(self, connections):
        """We creëren een graaf met voor elke verbinding een edge"""
        for conn in connections:
            self.add_edge(conn.station1, conn.station2, conn.distance)

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
        return distances

class DijkstraAlgorithm:
    def __init__(self, rail_network: RailNetwork, time_limit: int = None, max_routes: int = None):
        """
        Initialize DijkstraAlgorithm.
        Args:
            rail_network: The rail network to work with
            time_limit: Maximum time limit for routes in minutes (from config)
            max_routes: Maximum number of routes allowed (from config)
        """
        self.rail_network = rail_network
        self.time_limit = time_limit
        self.max_routes = max_routes
        self.graph = Graph()
        self.graph.add_connections(self.rail_network.connections)
    
    def calculate_start_station(self, start_stations, visited):
        """We zoeken een startstation dat nog niet bezocht is"""
        for conn in self.rail_network.connections:
            if conn.station1 not in start_stations and conn.station1 not in visited:
                start_stations.add(conn.station1)
                return(conn.station1)
            
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
        
        # Return None if no valid start station is found
        if start_station is None:
            return None, 0, visited_connections

        visited.add(start_station)

        while current_minutes < self.time_limit:
            next_station, shortest_distance = self.find_next_station(start_station, visited, visited_connections)

            if next_station is None or current_minutes + shortest_distance > self.time_limit:
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

        # Only return valid trajectories with at least one connection
        if len(current_traject) > 0:
            return current_traject, current_minutes, visited_connections
        return None, 0, visited_connections

    def k_value(self, trajects, visited_connections):
        """We berekenen de K"""
        total_connections = len(self.rail_network.connections)
        p = len(visited_connections) / total_connections
        T = len(trajects)
        total_minutes = sum(minutes for _, minutes in trajects)
        K = p * 10000 - (T * 100 + total_minutes)
        return K

    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Find best solution (single iteration since deterministic).
        """
        # Reset all connections
        for conn in self.rail_network.connections:
            conn.used = False

        # hier slaan we de trajecten op
        trajects = []

        # we houden de bezochte connecties bij
        visited_connections = set()

        # we maken een lege set om de stations in op te slaan die al als startstation gebruikt zijn
        start_stations = set()

        # Keep adding routes until we reach max_routes or can't find more valid routes
        valid_routes = 0
        while valid_routes < self.max_routes:
            result = self.traject(start_stations, visited_connections)
            if result is None or result[0] is None:
                break

            current_traject, current_minutes, new_connections = result
            if current_traject:
                trajects.append((current_traject, current_minutes))
                visited_connections = new_connections
                valid_routes += 1
            
            # Mark connections as used
            for start, end, _ in current_traject:
                for conn in self.rail_network.connections:
                    if {conn.station1, conn.station2} == {start, end}:
                        conn.used = True

        K = self.k_value(trajects, visited_connections)
        
        # Convert trajects to Route objects
        best_routes = []
        for traject_data in trajects:
            if not traject_data[0]:
                continue
            route = Route()
            current_time = 0
            for start, end, distance in traject_data[0]:
                # Find the actual Connection object and add it to the route
                for conn in self.rail_network.connections:
                    if {conn.station1, conn.station2} == {start, end}:
                        route.connections_used.add(conn)
                        if not route.stations:
                            route.stations.append(start)
                        route.stations.append(end)
                        current_time += conn.distance
                        break
            route.total_time = current_time
            if route.total_time > 0:
                best_routes.append(route)

        return K, best_routes