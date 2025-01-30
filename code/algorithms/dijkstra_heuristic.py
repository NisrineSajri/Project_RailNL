# dijkstra_heuristic.py

from heapq import heapify, heappop, heappush
from typing import List, Tuple, Set
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.connection import Connection

class DijkstraHeuristicAlgorithm:
    def __init__(self, rail_network: RailNetwork, time_limit: int = 120, max_routes: int = 7):
        """
        Initialiseert Dijkstra's algoritme met heuristiek
        Args:
            rail_network: rail network
            time_limit: maximale tijdsduur van trajecten
            max_routes: maximaal aantal routes
        """
        self.rail_network = rail_network
        self.time_limit = time_limit
        self.max_routes = max_routes

    def find_route(self, source: str, visited_connections: Set[Connection]) -> Route:
        """
        Zoekt naar een route via Dijkstra's Algoritme.
        We slaan doorlopen connecties over.
        We hebben een tijdslimiet.
        Eind station is het station met de verste distance vanaf source
        
        Args:
            source: start station berekend via calculate_start_station
            visited_connections: Set met al doorlopen connecties
            
        Returns:
            Route: De gecreërde route
        """        
        # we zetten de afstanden naar alle stations op oneindig
        distances = {station: float('inf') for station in self.rail_network.stations}
        
        # we stellen de afstand naar source gelijk aan 0
        distances[source] = 0

        # we maken een priority queue aan
        pq = [(0, source)]

        # we zetten het om in een queue object
        heapify(pq)

        # hier wordt opgeslagen hoe we bij elk station komen
        predecessors = {station: None for station in self.rail_network.stations}
        
        # we creëren een Route object met tijdslimiet
        route = Route(self.time_limit)

        # zolang de priority queue niet leeg is
        while len(pq) > 0:

            # we halen de node op met kortste afstand, dit wordt current_station (current_distance hoort hierbij)
            current_distance, current_station = heappop(pq) 

            # we stoppen als tijdslimiet is bereikt
            if current_distance > self.time_limit:
                break

            # we gaan alle bestaande connecties van current_station af
            for neighbor, connection in self.rail_network.stations[current_station].connections.items():

                # als de connectie al doorlopen is, gaan we naar de volgende
                if connection in visited_connections:
                    continue
                
                # we berekenen de nieuwe afstand
                distance = current_distance + connection.distance
                
                # als de afstand nu korter is, en binnen het tijdslimiet, vervangen we de afstand
                if distance < distances[neighbor] and distance <= self.time_limit:
                    distances[neighbor] = distance

                    # we voegen de afstand toe aan de priority que
                    heappush(pq, (distance, neighbor))
                    
                    # we slaan op via welke connectie we bij neighbor komen
                    predecessors[neighbor] = (current_station, connection)

        path = []
        end_station = None
        max_distance = 0
        
        # we kiezen als eindstation het station met de langste afstand vanaf source
        for station in distances:
            if distances[station] <= self.time_limit and predecessors[station] is not None:
                if distances[station] > max_distance:
                    max_distance = distances[station]
                    end_station = station

        # we slaan alle connecties op vanaf eind station
        while end_station is not None and predecessors[end_station] is not None:
            previous_station, connection = predecessors[end_station]
            path.append((previous_station, end_station, connection))
            end_station = previous_station

        path.reverse()
        # we voegen alle verbindingen van path toe aan de route
        for prev_station, next_station, connection in path:
            self.add_connection_to_route(route, connection)

        return route


    def calculate_start_station(self, visited_connections: Set[Connection]) -> str:
        """
        Kiest als start station eerst de stations die maar één connectie hebben.
        Daarna kiest als startstation het station met de minste ondoorlopen connecties.
        
        Args:
            visited_connections: Set met doorlopen connecties
            
        Returns:
            str: gekozen start station
        """
        # Dictionary om ondoorlopen verbindingen per station op te slaan
        start_stations = {}
        
        for conn in self.rail_network.connections:

            # we kijken alleen naar de ondoorlopen verbindingen
            if conn not in visited_connections:

                # voeg station 1 toe aan start_stations, als deze nog niet erin staat
                if conn.station1 not in start_stations:
                    start_stations[conn.station1] = 0

                # voeg station 2 toe aan start_stations, als deze nog niet erin staat
                if conn.station2 not in start_stations:
                    start_stations[conn.station2] = 0
                
                # we tellen 1 (ondoorlopen verbinding) op bij het station
                start_stations[conn.station1] += 1
                start_stations[conn.station2] += 1
        
        # als de dictionary leeg is, returnen we None
        if not start_stations:
            return None

        # We zoeken naar stations met 1 connectie
        for station, connection_count in start_stations.items():
            if connection_count == 1:
                return station
                
        # als geen station maar één connectie heeft, zoeken we naar station met de minste connecties
        min_connections = 0
        start_station = None
        
        for station, connection_count in start_stations.items():
            if connection_count < min_connections:
                min_connections = connection_count
                start_station = station
        
        # we returnen het station met de meest ondoorlopen verbindingen
        return start_station

    def add_connection_to_route(self, route: Route, connection: Connection) -> bool:
        """
        Voegt de juiste verbinding toe aan de route, zolang de route binnen het tijdslimiet blijft
        
        Args:
            route (Route): route waar verbinding aan wordt toegevoegd
            connection (Connection): de verbinding die toegevoegd moet worden
            
        Returns:
            bool: True als de verbinding is succesvol is toegevoegd, anders False
        """
        # we houden bij of tijdslimiet is overschreden
        if route.total_time + connection.distance > route.time_limit:
            return False

        # we updaten de totale tijd
        route.total_time += connection.distance

        # als de route leeg is, voegen we beide stations toe
        if not route.stations:
            route.stations.extend([connection.station1, connection.station2])

        else:
            # we pakken het laatste station uit de route
            last_station = route.stations[-1]
            # we willen de goede verbinding toevoegen
            if last_station == connection.station1:
                route.stations.append(connection.station2)
            elif last_station == connection.station2:
                route.stations.append(connection.station1)

            # als de eerste connectie verkeerd om is geplaatst, draaien we de connectie om
            elif len(route.stations) == 2:
                first_station = route.stations[0]
                if first_station == connection.station1:
                    route.stations[0], route.stations[-1] = route.stations[-1], route.stations[0]
                    route.stations.append(connection.station2)
                elif first_station == connection.station2:
                    route.stations[0], route.stations[-1] = route.stations[-1], route.stations[0]
                    route.stations.append(connection.station1)
            else:
                return False

        # we voegen de verbinding toe aan connections_used
        route.connections_used.add(connection)
        connection.used = True
        return True

    def find_best_solution(self, iterations: int = 1) -> Tuple[float, List[Route]]:
        """
        Zoekt naar de beste oplossing
        1 iteratie, want deterministisch
        
        Returns:
            Tuple[float, List[Route]]: Kwaliteit (K) en List met de routes
        """
        routes = []

        # we houden de bezochte connecties bij
        visited_connections = set()

        # zolang het maximale aantal routes niet overschreden wordt
        while len(routes) < self.max_routes:

            # we zoeken een start_station
            start_station = self.calculate_start_station(visited_connections)
            if start_station is None:
                break

            # we vinden de route vanaf start_station
            route = self.find_route(start_station, visited_connections)
            
            # als de route leeg is (geen verbindingen gebruikt)
            if not route.connections_used:
                break
            
            # we voegen de route toe aan routes en voegen de gebruikte connecties toe aan visited_connections
            routes.append(route)
            visited_connections.update(route.connections_used)

        routes = self.combine_routes(routes)

        # update rail_network met de routes
        self.rail_network.routes = routes
        # we berekenen de kwaliteit (K)
        quality = self.rail_network.calculate_quality()

        return quality, routes
        
    def combine_routes(self, routes: List[Route]) -> List[Route]:
        """
        Combineert routes als dit mogelijk is

        Args:
            List[Route]: List met alle berekende routes
            
        Returns:
            List[Route]: de List met de (gecombineerde) routes
        """
        if not routes:
            return routes
            
        i = 0
        while i < len(routes) - 1:
            route1 = routes[i]
            route2 = routes[i + 1]
            
            # We kijken of deze routes samen de tijd al overschreiden
            if route1.total_time + route2.total_time >= self.time_limit:
                i += 1
                continue
            
            # we pakken het laatste station van route 1 en het eerste station van route 2
            end_station = route1.stations[-1]
            start_station = route2.stations[0]
            
            # We kijken of deze twee station gecombineert kunnen worden
            connection = self.rail_network.stations[end_station].connections.get(start_station)
            
            # als de connectie bestaat en dit totale traject niet het tijdslimiet overschreidt
            if (connection and route1.total_time + route2.total_time + connection.distance <= self.time_limit):
                
                # we creëren en updaten alles van deze nieuwe route
                combined_route = Route(self.time_limit)
                combined_route.stations = route1.stations + route2.stations
                combined_route.connections_used = route1.connections_used | route2.connections_used
                combined_route.connections_used.add(connection)
                combined_route.total_time = route1.total_time + route2.total_time + connection.distance
                
                # we vervangen routes[i] door de gecombineerde route, en we verwijderen routes[i+1] uit routes
                routes[i] = combined_route
                routes.pop(i + 1)
            
            # als we geen connectie hebben gevonden om deze trajecten te verbinden
            else:
                i += 1
                
        return routes
    