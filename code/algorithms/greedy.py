import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now you can import from the classes module
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.station import Station
from constants import STATIONS_FILE, CONNECTIONS_FILE

class Greedy:
    def __init__(self, network: RailNetwork):
        self.network = network  # Bind the network to the Greedy class
        self.max_routes = 7
        self.max_time = 120  # Maximum time for a route in minutes

    def get_most_connections(self) -> list[Station]:
        """
        Get a list of stations sorted by the number of connections, from most to least.

        Returns:
            list[Station]: List of stations sorted by number of connections in descending order.
        """
        # Get all stations from the network
        stations = list(self.network.stations.values())
        
        # Sort all stations by the number of connections in descending order
        stations.sort(key=lambda station: len(station.connections), reverse=True)
        
        return stations


    def create_route(self, start_station: Station) -> Route:
        """
        Creates a single route starting from the given station.
        Ensures no station is visited more than once within this route.
        """
        route = Route()
        current_station = start_station.name
        visited_stations = set()  # Keep track of stations visited in this route

        while True:
            station = self.network.stations[current_station]
            visited_stations.add(current_station)  # Mark the station as visited

            # Get all valid connections that:
            # 1. Have not been used.
            # 2. Do not exceed the max time.
            # 3. Lead to stations not already visited in this route.
            possible_connections = []
            for _, conn in station.connections.items():
                if not conn.used and route.total_time + conn.distance <= self.max_time:
                    other_station = conn.get_other_station(current_station)
                    if other_station not in visited_stations:
                        possible_connections.append(conn)

            if not possible_connections:
                # No valid connections available, end the route
                break

            # Choose the best connection based on the number of unused connections at the destination
            best_connection = None
            max_unused_connections = -1

            for conn in possible_connections:
                other_station = conn.get_other_station(current_station)
                
                # Tel de onbenutte verbindingen met een for-loop en if-statement
                unused_connections = 0
                for c in self.network.stations[other_station].connections.values():
                    if not c.used:
                        unused_connections += 1
                
                # Als deze verbinding meer onbenutte verbindingen heeft, kies deze als de beste
                if unused_connections > max_unused_connections:
                    max_unused_connections = unused_connections
                    best_connection = conn

            # Add the best connection to the route
            if not route.add_connection(best_connection):
                break

            # Update the current station
            current_station = best_connection.get_other_station(current_station)

        return route


    def runGreedy(self):
        """
        Run the greedy algorithm to create routes using a sorted list of stations.
        """
        # Reset all connections
        for conn in self.network.connections:
            conn.used = False
        self.network.routes.clear()

        # Get the sorted list of stations by number of connections
        sorted_stations = self.get_most_connections()
        used_stations = set()  # Track stations already used as starting points

        for start_station in sorted_stations:
            # Check if the station has available connections
            if start_station.name in used_stations:
                # Station is al gebruikt
                pass
            else:
                all_connections_used = True
                for conn in start_station.connections.values():
                    if not conn.used:  # Als er een verbinding is die niet gebruikt is
                        all_connections_used = False
                        break  # Stop de loop zodra we een niet-gebruikte verbinding vinden

                if all_connections_used:
                    # Alle verbindingen zijn gebruikt
                    pass

            print(f"Starting with station: {start_station.name} with {len(start_station.connections)} connections")
            
            # Mark the station as used
            used_stations.add(start_station.name)

            # Create a route starting from the current station
            route = self.create_route(start_station)

            # Add the route to the network if it contains connections
            if route.connections_used:
                self.network.routes.append(route)

            # Check if the maximum number of routes has been reached
            if len(self.network.routes) >= self.max_routes:
                break

            # Check if all connections are used
            all_used = all(conn.used for conn in self.network.connections)
            if all_used:
                break

        # Calculate and return quality
        return self.network.calculate_quality()


# Main function for testing
if __name__ == "__main__":
    # Initialize the RailNetwork
    network = RailNetwork()

    # Load stations and connections
    network.load_stations(STATIONS_FILE)
    network.load_connections(CONNECTIONS_FILE)

    # Print initial network details
    print(f"Loaded {len(network.stations)} stations and {len(network.connections)} connections.")

    # Run the Greedy algorithm
    greedy = Greedy(network)
    quality = greedy.runGreedy()

    # Print routes
    print("\nRoutes created:")

    route_number = 1
    for route in network.routes:
        # Print current route number and route
        print("Route " + str(route_number) + ": " + str(route))
        route_number = route_number + 1

    # Print quality
    print("")
    print("Network quality: " + str(quality))