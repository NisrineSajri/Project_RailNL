import csv
import itertools
import matplotlib.pyplot as plt
from classes.rail_network import RailNetwork
from algorithms.hill_climber import HillClimber
from copy import deepcopy  # Import deepcopy voor volledige objectkopieën

def parameter_tuning(hill_climber_class, network, iterations_list, runs_list, max_routes_list, time_limit_list, output_file, plot_file):
    quality_scores = []

    # Genereer alle combinaties van parameters
    parameter_combinations = itertools.product(iterations_list, runs_list, max_routes_list, time_limit_list)

    for iterations, runs, max_routes, time_limit in parameter_combinations:
        print(f"Running for iterations={iterations}, runs={runs}, max_routes={max_routes}, time_limit={time_limit}...")

        run_scores = []

        # Run voor elke combinatie van parameters
        for run in range(runs):
            print(f"Run {run + 1}/{runs} started...")
            try:
                fresh_network = deepcopy(network)
                hill_climber = hill_climber_class(fresh_network, max_routes=max_routes, time_limit=time_limit)
                best_quality, _ = hill_climber.find_best_solution(iterations)
                run_scores.append(best_quality)
            except Exception as e:
                print(f"Error during run {run + 1}: {e}")
                run_scores.append(0)

        # Bereken de gemiddelde score voor de huidige combinatie van parameters
        avg_score = sum(run_scores) / len(run_scores)
        quality_scores.append((iterations, runs, max_routes, time_limit, avg_score))

    # Sla de resultaten op in een CSV-bestand
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Iterations", "Runs", "Max Routes", "Time Limit", "Average Quality Score"])
        for iteration, run, max_routes, time_limit, avg_score in quality_scores:
            writer.writerow([iteration, run, max_routes, time_limit, avg_score])

    # Plot de resultaten
    plt.figure(figsize=(12, 6))
    iterations = [x[0] for x in quality_scores]
    runs = [x[1] for x in quality_scores]
    max_routes = [x[2] for x in quality_scores]
    time_limit = [x[3] for x in quality_scores]
    avg_scores = [x[4] for x in quality_scores]

    scatter = plt.scatter(iterations, runs, c=avg_scores, cmap='viridis', s=100, label="Avg Score")
    plt.colorbar(scatter, label='Average Quality Score')
    plt.title("Parameter Tuning: HillClimber Quality Scores")
    plt.xlabel("Iterations")
    plt.ylabel("Runs")
    plt.grid(True)

    plt.savefig(plot_file)
    print(f"Plot saved to {plot_file}.")
    plt.close()

def load_network(stations_file: str, connections_file: str) -> RailNetwork:
    """
    Laad een RailNetwork met de gegeven stations- en verbindingenbestanden.
    
    Args:
        stations_file (str): Pad naar het stationsbestand.
        connections_file (str): Pad naar het verbindingenbestand.
    
    Returns:
        RailNetwork: Een geladen RailNetwork-object.
    
    Samenvatting:
        Laadt een RailNetwork met de opgegeven station- en verbindingenbestanden.
    """
    network = RailNetwork()
    network.load_stations(stations_file)
    network.load_connections(connections_file)
    return network

if __name__ == "__main__":
    # Holland dataset
    holland_stations = "../data/StationsHolland.csv"
    holland_connections = "../data/ConnectiesHolland.csv"

    # Nationaal dataset
    national_stations = "../data/StationsNationaal.csv"
    national_connections = "../data/ConnectiesNationaal.csv"

    # Laad Holland network
    holland_network = load_network(holland_stations, holland_connections)
    holland_output_csv = "holland_parameter_tuning_results.csv" 
    holland_plot_file = "holland_parameter_tuning_plot.png"
    print("Running Parameter Tuning for HillClimber on Holland network...")
    parameter_tuning(
        hill_climber_class=HillClimber,  # Alleen de klasse doorgeven, initialisatie gebeurt in de functie
        network=holland_network,
        iterations_list=[500, 1000, 1500],  # Verschillende iteraties om te testen
        runs_list=[500, 1000, 1500],  # Verschillende runs om te testen
        max_routes_list=[7, 7, 7],  # Testen met verschillende max_routes
        time_limit_list=[60, 100, 120],  # Testen met verschillende time_limits
        output_file=holland_output_csv,
        plot_file=holland_plot_file,
    )

    # Laad Nationaal network
    national_network = load_network(national_stations, national_connections)
    national_output_csv = "national_parameter_tuning_results.csv"
    national_plot_file = "national_parameter_tuning_plot.png"
    print("Running Parameter Tuning for HillClimber on National network...")
    parameter_tuning(
        hill_climber_class=HillClimber,  # Alleen de klasse doorgeven, initialisatie gebeurt in de functie
        network=national_network,
        iterations_list=[500, 1000, 1500],  # Verschillende iteraties om te testen
        runs_list=[500, 1000, 1500],  # Verschillende runs om te testen
        max_routes_list=[10, 16, 20],  # Testen met verschillende max_routes
        time_limit_list=[100, 120, 180],  # Testen met verschillende time_limits
        output_file=national_output_csv,
        plot_file=national_plot_file,
    )
