import csv
from classes.rail_network import RailNetwork  
from algorithms.hill_climber import HillClimber

def run_multiple_times(network: RailNetwork, iterations: int, runs: int, output_file: str):
    """
    Voer het HillClimber-algoritme meerdere keren uit en sla de resultaten op in een CSV-bestand.
    
    Args:
        network (RailNetwork): Het spoornetwerk om op te werken.
        iterations (int): Aantal iteraties per HillClimber-run.
        runs (int): Aantal keren dat het algoritme wordt uitgevoerd.
        output_file (str): Bestandsnaam voor de CSV-output.
    """
    quality_scores = []

    for run in range(runs):
        print(f"Run {run + 1}/{runs} gestart...")
        hill_climber = HillClimber(network)
        quality, _ = hill_climber.find_single_solution(iterations=iterations)
        quality_scores.append(quality)
        print(f"Run {run + 1}/{runs} voltooid met kwaliteitsscore: {quality}")

    # Schrijf resultaten naar een CSV-bestand
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Header 1 , score onder elkaar 
        writer.writerow(["Run", "Quality Score"])
        # retourt (index, waarde)  
        for i, score in enumerate(quality_scores):
            writer.writerow([i + 1, score])

    print(f"Alle runs voltooid. Resultaten opgeslagen in {output_file}.")

# Gebruik het script
if __name__ == "__main__":
    rail_network = RailNetwork()  
    
    # Parameters

    # Aantal iteraties per run
    num_iterations = 1000  
    # Hoe vaak HillClimber wordt uitgevoerd
    num_runs = 10  
    
    output_csv = "hill_climber_results.csv"

    # Voer HillClimber meerdere keren uit
    run_multiple_times(
        network=rail_network,
        iterations=num_iterations,
        runs=num_runs,
        output_file=output_csv
    )
