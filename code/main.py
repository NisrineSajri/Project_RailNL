from classes.rail_network import RailNetwork
from constants import STATIONS_FILE, CONNECTIONS_FILE

def print_solution_stats(network, quality, routes):
    """Print detailed statistics about the solution"""
    total_time = sum(route.total_time for route in routes)
    coverage_cost = len(routes) * 100 + total_time
    p = (quality + coverage_cost) / 10000
    
    print("\nSolution Statistics:")
    print(f"Quality Score (K): {quality:.2f}")
    print(f"Number of routes (T): {len(routes)}")
    print(f"Total time (Min): {total_time} minutes")
    print(f"Connection coverage (p): {p:.4f} ({p*100:.1f}%)")
    
    print("\nRoutes:")
    for i, route in enumerate(routes, 1):
        print(f"{i}. {route}")

def main():
    """
    Main function to run the railway optimization.
    """
    network = RailNetwork()
    network.load_stations(STATIONS_FILE)
    network.load_connections(CONNECTIONS_FILE)
    
    best_quality, best_routes = network.find_best_solution(iterations=1000)
    print_solution_stats(network, best_quality, best_routes)

if __name__ == "__main__":
    main()