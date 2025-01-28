import os
import sys
import csv
from typing import List, Tuple
import matplotlib.pyplot as plt

# Voeg de bovenliggende map toe aan het Python-pad zodat we de klassen kunnen importeren
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Get the code directory
sys.path.append(parent_dir)

from classes.rail_network import RailNetwork
from algorithms.beam_greedy import BeamSearchAlgorithm
from algorithms.beam_greedy_random import BeamSearchAlgorithmV2
from algorithms.beam_heuristics_random import BeamSearchAlgorithmV3
from constants import NATIONAL_CONFIG

def analyze_beam_width(min_width: int = 1, max_width: int = 9, runs_per_width: int = 5) -> List[Tuple[int, float]]:
    """
    Analyseer de prestaties van Beam Search V1 bij verschillende breedtes.

    Args:
        min_width (int): De minimale beam breedte die getest moet worden. Standaardwaarde is 1.
        max_width (int): De maximale beam breedte die getest moet worden. Standaardwaarde is 9.
        runs_per_width (int): Het aantal uitvoeringen per beam breedte. Standaardwaarde is 5.

    Returns:
        List[Tuple[int, float]]: Een lijst met tuples waarin elke tuple de breedte bevat 
        en de gemiddelde kwaliteitsscore voor die breedte.
    """
    network = RailNetwork()
    network.load_stations(NATIONAL_CONFIG['stations_file'])
    network.load_connections(NATIONAL_CONFIG['connections_file'])
    
    results = []
    for width in range(min_width, max_width + 1):
        print(f"\nTesting V1 beam width {width}...")
        width_scores = []
        
        for run in range(runs_per_width):
            algorithm = BeamSearchAlgorithm(
                network,
                beam_width=width,
                time_limit=NATIONAL_CONFIG['time_limit'],
                max_routes=NATIONAL_CONFIG['max_routes']
            )
            quality, _ = algorithm.find_best_solution()
            width_scores.append(quality)
            print(f"Run {run + 1}: Quality = {quality:.2f}")
        
        avg_quality = sum(width_scores) / len(width_scores)
        results.append((width, avg_quality))
        print(f"Average quality for width {width}: {avg_quality:.2f}")
    
    return results

def analyze_beam_width_v2(min_width: int = 1, max_width: int = 9, runs_per_width: int = 5) -> List[Tuple[int, float]]:
    """
    Analyseer de prestaties van Beam Search V2 bij verschillende breedtes.

    Args:
        min_width (int): De minimale beam breedte die getest moet worden. Standaardwaarde is 1.
        max_width (int): De maximale beam breedte die getest moet worden. Standaardwaarde is 9.
        runs_per_width (int): Het aantal uitvoeringen per beam breedte. Standaardwaarde is 5.

    Returns:
        List[Tuple[int, float]]: Een lijst met tuples waarin elke tuple de breedte bevat 
        en de gemiddelde kwaliteitsscore voor die breedte.
    """
    network = RailNetwork()
    network.load_stations(NATIONAL_CONFIG['stations_file'])
    network.load_connections(NATIONAL_CONFIG['connections_file'])
    
    results = []
    for width in range(min_width, max_width + 1):
        print(f"\nTesting V2 beam width {width}...")
        width_scores = []
        
        for run in range(runs_per_width):
            algorithm = BeamSearchAlgorithmV2(
                network,
                beam_width=width,
                time_limit=NATIONAL_CONFIG['time_limit'],
                max_routes=NATIONAL_CONFIG['max_routes']
            )
            quality, _ = algorithm.find_best_solution()
            width_scores.append(quality)
            print(f"Run {run + 1}: Quality = {quality:.2f}")
        
        avg_quality = sum(width_scores) / len(width_scores)
        results.append((width, avg_quality))
        print(f"Average quality for width {width}: {avg_quality:.2f}")
    
    return results

def analyze_beam_width_v3(min_width: int = 1, max_width: int = 9, runs_per_width: int = 5) -> List[Tuple[int, float]]:
    """
    Analyseer de prestaties van HeuristicRandomBFS (Beam Search V3) bij verschillende breedtes.

    Args:
        min_width (int): De minimale beam breedte die getest moet worden. Standaardwaarde is 1.
        max_width (int): De maximale beam breedte die getest moet worden. Standaardwaarde is 9.
        runs_per_width (int): Het aantal uitvoeringen per beam breedte. Standaardwaarde is 5.

    Returns:
        List[Tuple[int, float]]: Een lijst met tuples waarin elke tuple de breedte bevat 
        en de gemiddelde kwaliteitsscore voor die breedte.
    """
    network = RailNetwork()
    network.load_stations(NATIONAL_CONFIG['stations_file'])
    network.load_connections(NATIONAL_CONFIG['connections_file'])
    
    results = []
    for width in range(min_width, max_width + 1):
        print(f"\nTesting V3 beam width {width}...")
        width_scores = []
        
        for run in range(runs_per_width):
            algorithm = BeamSearchAlgorithmV3(
                network,
                time_limit=NATIONAL_CONFIG['time_limit'],
                max_routes=NATIONAL_CONFIG['max_routes']
            )
            quality, _ = algorithm.find_best_solution(iterations=100)  # Use iterations for randomization
            width_scores.append(quality)
            print(f"Run {run + 1}: Quality = {quality:.2f}")
        
        avg_quality = sum(width_scores) / len(width_scores)
        results.append((width, avg_quality))
        print(f"Average quality for width {width}: {avg_quality:.2f}")
    
    return results

def plot_comparison(results1: List[Tuple[int, float]], results2: List[Tuple[int, float]], 
                   results3: List[Tuple[int, float]], filename: str = 'beam_search_comparison.png'):
    """
    Genereer en sla een grafiek op waarin de prestaties van de drie versies van Beam Search worden vergeleken.

    Args:
        results1 (List[Tuple[int, float]]): Resultaten van Beam Search V1.
        results2 (List[Tuple[int, float]]): Resultaten van Beam Search V2.
        results3 (List[Tuple[int, float]]): Resultaten van HeuristicRandomBFS (Beam Search V3).
        filename (str): De naam van het bestand waarin de grafiek wordt opgeslagen. Standaardwaarde is 'beam_search_comparison.png'.

    Returns:
        None: Slaat de gegenereerde grafiek op als een afbeelding in de map 'results'.
    """
    widths1, qualities1 = zip(*results1)
    widths2, qualities2 = zip(*results2)
    widths3, qualities3 = zip(*results3)
    
    plt.figure(figsize=(12, 7))
    plt.plot(widths1, qualities1, 'bo-', label='Beam Search V1')
    plt.plot(widths2, qualities2, 'ro-', label='Beam Search V2')
    plt.plot(widths3, qualities3, 'go-', label='Beam Search V3 (HeuristicBFS)')
    plt.xlabel('Beam Width (k)')
    plt.ylabel('Average Quality Score')
    plt.title('Beam Search Performance Comparison')
    plt.legend()
    plt.grid(True)
    
    results_dir = os.path.join(current_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    plt.savefig(os.path.join(results_dir, filename))
    plt.close()

def save_comparison_results(results1: List[Tuple[int, float]], results2: List[Tuple[int, float]], 
                          results3: List[Tuple[int, float]], filename: str = 'beam_search_comparison.csv'):
    """
    Sla de vergelijking van resultaten van de drie versies van Beam Search op in een CSV-bestand.

    Args:
        results1 (List[Tuple[int, float]]): Resultaten van Beam Search V1.
        results2 (List[Tuple[int, float]]): Resultaten van Beam Search V2.
        results3 (List[Tuple[int, float]]): Resultaten van HeuristicRandomBFS (Beam Search V3).
        filename (str): De naam van het bestand waarin de resultaten worden opgeslagen. Standaardwaarde is 'beam_search_comparison.csv'.

    Returns:
        None: Slaat de resultaten op in de map 'results' als een CSV-bestand.
    """
    results_dir = os.path.join(current_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Beam Width', 'V1 Quality', 'V2 Quality', 'V3 Quality'])
        for (w1, q1), (w2, q2), (w3, q3) in zip(results1, results2, results3):
            writer.writerow([w1, q1, q2, q3])

if __name__ == "__main__":
    print("Analyzing Beam Search V1...")
    results_v1 = analyze_beam_width(min_width=1, max_width=9, runs_per_width=5)
    
    print("\nAnalyzing Beam Search V2...")
    results_v2 = analyze_beam_width_v2(min_width=1, max_width=9, runs_per_width=5)
    
    print("\nAnalyzing Beam Search V3 (HeuristicBFS)...")
    results_v3 = analyze_beam_width_v3(min_width=1, max_width=9, runs_per_width=5)
    
    # Sla resultaten op
    save_comparison_results(results_v1, results_v2, results_v3)
    plot_comparison(results_v1, results_v2, results_v3)
    
    # Print de beste configurations
    best_width_v1, best_quality_v1 = max(results_v1, key=lambda x: x[1])
    best_width_v2, best_quality_v2 = max(results_v2, key=lambda x: x[1])
    best_width_v3, best_quality_v3 = max(results_v3, key=lambda x: x[1])
    
    print("\nResults Summary:")
    print(f"Beam Search V1 - Best width: {best_width_v1}, Best quality: {best_quality_v1:.2f}")
    print(f"Beam Search V2 - Best width: {best_width_v2}, Best quality: {best_quality_v2:.2f}")
    print(f"Beam Search V3 - Best width: {best_width_v3}, Best quality: {best_quality_v3:.2f}")