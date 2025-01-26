import csv
import matplotlib.pyplot as plt
from classes.rail_network import RailNetwork
from algorithms.hill_climber import HillClimber

def run_multiple_times(network: RailNetwork, iterations: int, runs: int, output_file: str, plot_file: str):
    """
    Voer het HillClimber-algoritme meerdere keren uit, sla de resultaten op in een CSV-bestand en genereer een staafdiagram.
    
    Args:
        network (RailNetwork): Het spoornetwerk om mee te werken.
        iterations (int): Aantal iteraties per HillClimber-run.
        runs (int): Aantal keren dat het algoritme wordt uitgevoerd.
        output_file (str): Bestandsnaam voor de CSV-uitvoer.
        plot_file (str): Bestandsnaam voor de afbeelding van het diagram.
    """
    quality_scores = []

    for run in range(runs):
        print(f"Run {run + 1}/{runs} started...")
        hill_climber = HillClimber(network, seed=None)  # Willekeurige resultaten
        quality, _ = hill_climber.find_best_solution(iterations=iterations)
        quality_scores.append(quality)
        print(f"Run {run + 1}/{runs} completed with quality score: {quality}")

   # Sla de resultaten op in een CSV-bestand
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "Quality Score"])
        for i, score in enumerate(quality_scores):
            writer.writerow([i + 1, score])

    print(f"Results saved to {output_file}.")

    # Genereer een barplot van de quality scores
    plt.bar(range(1, runs + 1), quality_scores, color='lightblue', label='Quality Score')
    plt.title("HillClimber Quality Scores")
    plt.xlabel("Run")
    plt.ylabel("Quality Score")
    plt.grid(True, axis='y')
    plt.legend()
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
    holland_output_csv = "holland_results.csv"
    holland_plot_file = "holland_plot.png"
    print("Running HillClimber for Holland network...")
    run_multiple_times(
        network=holland_network,
        # Hoeveelheid iteraties per run
        iterations=1000,  
        # Hoeveelheid runs
        runs=1000000, 
        output_file=holland_output_csv,
        plot_file=holland_plot_file,
    )

    # Laad Nationaal network
    national_network = load_network(national_stations, national_connections)
    national_output_csv = "national_results.csv"
    national_plot_file = "national_plot.png"
    print("Running HillClimber for National network...")
    run_multiple_times(
        network=national_network,
        # Hoeveelheid iteraties per run
        iterations=1000,  
        # Hoeveelheid runs
        runs=1000000, 
        output_file=national_output_csv,
        plot_file=national_plot_file,
    )
