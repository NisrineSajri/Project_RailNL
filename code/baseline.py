import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import seaborn as sns
import argparse
from collections import defaultdict
from classes.rail_network import RailNetwork
from algorithms.random_algorithm import RandomAlgorithm
from constants import HOLLAND_CONFIG, NATIONAL_CONFIG

def analyze_random_solutions(config: dict, iterations: int = 1000, seed: int = 42) -> Tuple[List[float], dict]:
    """
    Run multiple iterations of the random algorithm and analyze the results.
    
    Args:
        config (dict): Configuration dictionary with dataset-specific settings
        iterations (int): Number of random solutions to generate
        seed (int): Random seed for reproducibility
        
    Returns:
        Tuple[List[float], dict]: List of scores and dictionary with statistics
    """
    # Set random seed for reproducibility
    np.random.seed(seed)
    
    # Initialize network and algorithm
    network = RailNetwork()
    network.load_stations(config['stations_file'])
    network.load_connections(config['connections_file'])
    
    algorithm = RandomAlgorithm(network)
    
    # Monkey patch create_route to use correct time limit
    original_create_route = algorithm.create_route
    def create_route_wrapper(*args, **kwargs):
        return original_create_route(*args, time_limit=config['time_limit'], **kwargs)
    algorithm.create_route = create_route_wrapper
    
    # Collect scores
    scores = []
    route_counts = defaultdict(int)
    connection_counts = defaultdict(int)
    
    for _ in range(iterations):
        quality = algorithm.create_solution(max_routes=config['max_routes'])
        scores.append(quality)
        
        # Track statistics about the solution
        route_counts[len(network.routes)] += 1
        total_connections = sum(1 for conn in network.connections if conn.used)
        connection_counts[total_connections] += 1
    
    # Calculate statistics
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

def plot_results(scores: List[float], stats: dict, dataset: str, save_path: str = None):
    """
    Create visualizations of the random algorithm results.
    
    Args:
        scores (List[float]): List of quality scores
        stats (dict): Dictionary containing statistics
        dataset (str): Name of the dataset being analyzed
        save_path (str, optional): Path to save the plot
    """
    plt.figure(figsize=(15, 15))
    
    # Plot 1: Score progression
    plt.subplot(3, 1, 1)
    plt.plot(range(len(scores)), scores, alpha=0.7, color='#0B2447')
    plt.axhline(stats['mean'], color='#ff4444', linestyle='--', 
                label=f'Mean: {stats["mean"]:.2f} (σ: {stats["std"]:.2f})')
    plt.title(f'Score Progression over Iterations - {dataset.upper()} Dataset')
    plt.xlabel('Iteration')
    plt.ylabel('Quality Score')
    plt.legend()
    
    # Plot 2: Distribution of scores
    plt.subplot(3, 1, 2)
    sns.histplot(scores, kde=True, color='#0B2447', bins=30)
    plt.axvline(stats['mean'], color='#ff4444', linestyle='--', 
                label=f'Mean: {stats["mean"]:.2f} (σ: {stats["std"]:.2f})')
    plt.title('Distribution of Quality Scores')
    plt.xlabel('Quality Score')
    plt.ylabel('Count')
    plt.legend()
    
    # Plot 3: Route count distribution
    plt.subplot(3, 1, 3)
    route_counts = stats['route_distribution']
    plt.bar(route_counts.keys(), route_counts.values(), color='#0B2447', alpha=0.7)
    plt.axvline(stats['avg_routes'], color='#ff4444', linestyle='--',
                label=f'Avg Routes: {stats["avg_routes"]:.2f}')
    plt.title('Distribution of Route Counts')
    plt.xlabel('Number of Routes')
    plt.ylabel('Frequency')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
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
    
    # Select configuration based on dataset
    config = HOLLAND_CONFIG if args.dataset == 'holland' else NATIONAL_CONFIG
    
    # Run analysis
    scores, stats = analyze_random_solutions(config, iterations=args.iterations, seed=args.seed)
    
    # Print statistics
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
    
    # Create visualization
    plot_results(scores, stats, args.dataset, 
                save_path=f"baseline_analysis_{args.dataset}.png")

if __name__ == "__main__":
    main()