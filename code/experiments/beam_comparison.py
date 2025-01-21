import os
import sys
import csv
from typing import List, Tuple
import matplotlib.pyplot as plt

# Add the parent directory to Python path so we can import the classes
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Get the code directory
sys.path.append(parent_dir)

from classes.rail_network import RailNetwork
from algorithms.beam_search import BeamSearchAlgorithm
from algorithms.beam_search_v2 import BeamSearchAlgorithmV2
from constants import NATIONAL_CONFIG

def analyze_beam_width(min_width: int = 1, max_width: int = 9, runs_per_width: int = 5) -> List[Tuple[int, float]]:
    """
    Analyze beam search V1 performance for different beam widths.
    """
    # Initialize network
    network = RailNetwork()
    network.load_stations(NATIONAL_CONFIG['stations_file'])
    network.load_connections(NATIONAL_CONFIG['connections_file'])
    
    results = []
    
    # Test each beam width
    for width in range(min_width, max_width + 1):
        print(f"\nTesting beam width {width}...")
        width_scores = []
        
        # Multiple runs for each width
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
    Analyze beam search V2 performance for different beam widths.
    """
    # Initialize network
    network = RailNetwork()
    network.load_stations(NATIONAL_CONFIG['stations_file'])
    network.load_connections(NATIONAL_CONFIG['connections_file'])
    
    results = []
    
    # Test each beam width
    for width in range(min_width, max_width + 1):
        print(f"\nTesting beam width {width}...")
        width_scores = []
        
        # Multiple runs for each width
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

def plot_comparison(results1: List[Tuple[int, float]], results2: List[Tuple[int, float]], 
                   filename: str = 'beam_search_comparison.png'):
    """Plot and save the comparison results."""
    widths1, qualities1 = zip(*results1)
    widths2, qualities2 = zip(*results2)
    
    plt.figure(figsize=(12, 7))
    plt.plot(widths1, qualities1, 'bo-', label='Beam Search V1')
    plt.plot(widths2, qualities2, 'ro-', label='Beam Search V2')
    plt.xlabel('Beam Width (k)')
    plt.ylabel('Average Quality Score')
    plt.title('Beam Search Performance Comparison')
    plt.legend()
    plt.grid(True)
    
    # Save in the experiments/results directory
    results_dir = os.path.join(current_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    plt.savefig(os.path.join(results_dir, filename))
    plt.close()

def save_comparison_results(results1: List[Tuple[int, float]], results2: List[Tuple[int, float]], 
                          filename: str = 'beam_search_comparison.csv'):
    """Save comparison results to CSV file."""
    # Create results directory if it doesn't exist
    results_dir = os.path.join(current_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Beam Width', 'V1 Quality', 'V2 Quality'])
        for (w1, q1), (w2, q2) in zip(results1, results2):
            writer.writerow([w1, q1, q2])

if __name__ == "__main__":
    # Run analysis for both versions
    print("Analyzing Beam Search V1...")
    results_v1 = analyze_beam_width(min_width=1, max_width=9, runs_per_width=5)
    
    print("\nAnalyzing Beam Search V2...")
    results_v2 = analyze_beam_width_v2(min_width=1, max_width=9, runs_per_width=5)
    
    # Create results directory and save results
    save_comparison_results(results_v1, results_v2)
    plot_comparison(results_v1, results_v2)
    
    # Print best configurations
    best_width_v1, best_quality_v1 = max(results_v1, key=lambda x: x[1])
    best_width_v2, best_quality_v2 = max(results_v2, key=lambda x: x[1])
    
    print("\nResults Summary:")
    print(f"Beam Search V1 - Best width: {best_width_v1}, Best quality: {best_quality_v1:.2f}")
    print(f"Beam Search V2 - Best width: {best_width_v2}, Best quality: {best_quality_v2:.2f}")