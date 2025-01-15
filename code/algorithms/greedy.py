import random
from typing import List, Tuple

from classes.rail_network import RailNetwork
from classes.route import Route
from classes.station import Station

class Greedy:
    def __init__(self, network: RailNetwork):
        self.network = network  # Bind the network to the Greedy class
        self.max_routes = 7
        self.max_time = 120  # Maximum time for a route in minutes

    def get_most_connections(self):
        """
        Find the station with the most connections.

        Returns:
            Station: The station with the most connections
        """
        # De laagst mogelijke hoeveelheid connecties
        max_connections = -1
        station_with_max_connections = None

        for station in self.network.stations.values():
            num_connections = len(station.connections)
            if num_connections > max_connections:
                max_connections = num_connections
                station_with_max_connections = station

        return station_with_max_connections

    def create_route(self, start_station: Station) -> Route:
        """
        Creates a single route starting from the given station.
        """
        route = Route()
        current_station = start_station.name
        # Keep track of visited stations
        visited_stations = set()  

        while True:
            station = self.network.stations[current_station]
            # Mark the current station as visited
            visited_stations.add(current_station)  

            # Get all valid possible connections from the current station
            possible_connections = []
            for _, conn in station.connections.items():
                dest_station_name = conn.get_other_station(current_station)
                if (
                    not conn.used and 
                    route.total_time + conn.distance <= self.max_time and
                    dest_station_name not in visited_stations  # Ensure station isn't revisited
                ):
                    possible_connections.append(conn)

            if not possible_connections:
                break

            # Sort connections by unused connections at the destination
            scored_connections = []
            for conn in possible_connections:
                dest_station_name = conn.get_other_station(current_station)
                dest_station = self.network.stations[dest_station_name]

                # Count unused connections at the destination station
                unused_connections = 0
                for c in dest_station.connections.values():
                    if not c.used:
                        unused_connections += 1

                scored_connections.append((unused_connections, conn))

            if not scored_connections:
                break

            best_connection = None
            best_unused_count = -1

            for unused_connections, conn in scored_connections:
                if unused_connections > best_unused_count:
                    best_unused_count = unused_connections
                    best_connection = conn

            if best_connection is None or not route.add_connection(best_connection):
                break

            current_station = best_connection.get_other_station(current_station)

        return route

    def runGreedy(self):
        """
        Run the greedy algorithm to create routes.
        """
        # Reset alle connections
        for conn in self.network.connections:
            conn.used = False
        self.network.routes.clear()

        # Get starting station (one with the most connections)
        start_station = self.get_most_connections()
        print(f"Starting with station: {start_station.name} with {len(start_station.connections)} connections")

        while len(self.network.routes) < self.max_routes:
            # Create a route starting from the current station
            route = self.create_route(start_station)

            if not route.connections_used:
                # If we couldn't create a route, find the next station with the most unused connections
                unused_found = False
                for station in sorted(
                    self.network.stations.values(),
                    key=lambda s: sum(1 for c in s.connections.values() if not c.used),
                    reverse=True,
                ):
                    if any(not conn.used for conn in station.connections.values()):
                        start_station = station
                        unused_found = True
                        break

                if not unused_found:
                    break
            else:
                self.network.routes.append(route)
                # Update start_station to the station with the most unused connections
                start_station = max(
                    self.network.stations.values(),
                    key=lambda s: sum(1 for c in s.connections.values() if not c.used),
                )

            # Check if all connections are used
            if all(conn.used for conn in self.network.connections):
                break

        # Calculate and return quality
        return self.network.calculate_quality()