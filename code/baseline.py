import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import seaborn as sns
import argparse
import os
import json
from collections import defaultdict
from classes.rail_network import RailNetwork
from algorithms.random_algorithm import RandomAlgorithm
from constants import HOLLAND_CONFIG, NATIONAL_CONFIG

# Zorg ervoor dat de visualization directory bestaat
visualization_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'visualization')
os.makedirs(visualization_dir, exist_ok=True)

def load_algorithm_results(dataset: str) -> Dict[str, float]:
    """
    Laad de resultaten van alle algoritmes uit de results directory.
    
    Args:
        dataset (str): Dataset naam ('holland' of 'national')
    
    Returns:
        Dict[str, float]: Dictionary met gemiddelde scores per algoritme
    """
    experiments_dir = os.path.join('code', 'experiments', 'results')
    algorithm_means = {}
    
    # Loop door elke algoritme directory
    for algo_dir in os.listdir(experiments_dir):
        algo_path = os.path.join(experiments_dir, algo_dir)
        if os.path.isdir(algo_path):
            scores = []
            # Zoek alle JSON bestanden voor deze dataset
            for file in os.listdir(algo_path):
                if file.startswith(f"{dataset}_") and file.endswith(".json"):
                    with open(os.path.join(algo_path, file), 'r') as f:
                        data = json.load(f)
                        scores.extend([r['score'] for r in data['results'] if r['score'] is not None])
            
            if scores:  # Als we scores hebben gevonden
                algorithm_means[algo_dir] = np.mean(scores)
    
    return algorithm_means

def analyze_random_solutions(config: dict, iterations: int = 10000000000, seed: int = 42) -> Tuple[List[float], dict]:
    """
    Run multiple iterations of the random algorithm and analyze the results.
    
    Args:
        config (dict): Configuration dictionary with dataset-specific settings
        iterations (int): Number of random solutions to generate
        seed (int): Random seed for reproducibility
        
    Returns:
        Tuple[List[float], dict]: List of scores and dictionary with statistics
    """
    # Zet de random seed voor reproduceerbaarheid
    np.random.seed(seed)
    
    # Initialiseer netwerk en algoritme
    network = RailNetwork()
    network.load_stations(config['stations_file'])
    network.load_connections(config['connections_file'])
    
    algorithm = RandomAlgorithm(
        network,
        time_limit=config['time_limit'],
        max_routes=config['max_routes']
    )
    
    # Verzamel scores
    scores = []
    route_counts = defaultdict(int)
    connection_counts = defaultdict(int)
    
    for _ in range(iterations):
        quality = algorithm.create_solution(max_routes=config['max_routes'])
        scores.append(quality)
        
        # Volg statistieken over de oplossing
        route_counts[len(network.routes)] += 1
        total_connections = sum(1 for conn in network.connections if conn.used)
        connection_counts[total_connections] += 1
    
    # Bereken statistieken
    stats = {
        'mean': np.mean(scores),
        'std': np.std(scores),
        'min': np.min(scores),
        'max': np.max(scores),
        'avg_routes': sum(k * v for k, v in route_counts.items()) / iterations,
        'avg_connections': sum(k * v for k, v in connection_counts.items()) / iterations,
        'route_distribution': dict(route_counts),
        'connection_distribution': dict(connection_counts)
    }
    
    return scores, stats

def plot_results(scores: List[float], stats: dict, dataset: str, algorithm_means: Dict[str, float], save_path: str = None):
    """
    Create visualizations of the random algorithm results with algorithm comparisons.
    
    Args:
        scores (List[float]): List of quality scores
        stats (dict): Dictionary containing statistics
        dataset (str): Name of the dataset being analyzed
        algorithm_means (Dict[str, float]): Dictionary with mean scores per algorithm
        save_path (str, optional): Path to save the plot
    """
    plt.figure(figsize=(15, 8))
    
    # Plot: Verdeling van scores
    sns.histplot(scores, kde=True, color='#0B2447', bins=30, alpha=0.6)
    
    # Voeg baseline gemiddelde toe
    plt.axvline(stats['mean'], color='#ff4444', linestyle='--', 
                label=f'Baseline Mean: {stats["mean"]:.2f} (σ: {stats["std"]:.2f})')
    
    # Kleurenmap voor verschillende algoritmes
    colors = ['#2ecc71', '#3498db', '#9b59b6', '#f1c40f', '#e74c3c', '#1abc9c', '#e67e22', '#34495e']
    color_idx = 0
    
    # Voeg verticale lijnen toe voor elk algoritme
    for algo, mean in algorithm_means.items():
        # Bereken het percentiel van dit algoritme in de baseline verdeling
        percentile = 100 * (1 - (sum(score <= mean for score in scores) / len(scores)))
        percentile_text = f"{algo}: {mean:.2f} (p{percentile:.1f})"
        
        plt.axvline(mean, color=colors[color_idx], linestyle='-', 
                   label=percentile_text)
        color_idx = (color_idx + 1) % len(colors)
    
    plt.title(f'Kwaliteitsscore Verdeling - {dataset.upper()} Dataset\nmet Algorithm Vergelijking')
    plt.xlabel('Kwaliteitsscore')
    plt.ylabel('Aantal')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Analyze random solutions for rail network optimization')
    parser.add_argument('--dataset', type=str, choices=['holland', 'national'],
                      default='holland', help='Dataset to analyze (default: holland)')
    parser.add_argument('--iterations', type=int, default=1000,
                      help='Number of iterations (default: 1000)')
    parser.add_argument('--seed', type=int, default=42,
                      help='Random seed (default: 42)')
    
    args = parser.parse_args()
    
    # Selecteer de configuratie op basis van de dataset
    config = HOLLAND_CONFIG if args.dataset == 'holland' else NATIONAL_CONFIG
    
    # Laad resultaten van andere algoritmes
    algorithm_means = load_algorithm_results(args.dataset)
    
    # Voer de analyse uit
    scores, stats = analyze_random_solutions(config, iterations=args.iterations, seed=args.seed)
    
    # Print statistieken
    print(f"\nRandom Algorithm Statistics - {args.dataset.upper()} Dataset:")
    print(f"Number of iterations: {args.iterations}")
    print(f"Time limit per route: {config['time_limit']} minutes")
    print(f"Maximum routes allowed: {config['max_routes']}")
    print(f"Mean score: {stats['mean']:.2f}")
    print(f"Standard deviation: {stats['std']:.2f}")
    print(f"Min score: {stats['min']:.2f}")
    print(f"Max score: {stats['max']:.2f}")
    print(f"Average number of routes: {stats['avg_routes']:.2f}")
    print(f"Average connections used: {stats['avg_connections']:.2f}")
    
    print("\nAlgorithm Comparisons:")
    for algo, mean in algorithm_means.items():
        print(f"{algo}: {mean:.2f}")
    
    # Maak visualisatie en sla op in visualization directory
    save_path = os.path.join(visualization_dir, f"baseline_analysis_{args.dataset}.png")
    plot_results(scores, stats, args.dataset, algorithm_means, save_path=save_path)
    print(f"Visualization saved to {save_path}")

if __name__ == "__main__":
    main()