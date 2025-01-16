# main.py
import argparse
from typing import List, Type
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from classes.rail_network import RailNetwork
from classes.solution_statistics import SolutionStatistics
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.bfs_greedy import SimplifiedBFSAlgorithm
from algorithms.bfs_greedy_v2 import SimplifiedBFSAlgorithm as SimplifiedBFSAlgorithmV2
from algorithms.beam_search import BeamSearchAlgorithm
from algorithms.beam_search_v2 import BeamSearchAlgorithmV2
from constants import STATIONS_FILE, CONNECTIONS_FILE


def run_algorithm(algorithm_class, network: RailNetwork, iterations: int = None) -> None:
    """
    Run the specified algorithm and print its results.
    
    Args:
        algorithm_class: Class of the algorithm to run
        network: RailNetwork instance
        iterations: Number of iterations (only used for RandomAlgorithm)
    """
    algorithm = algorithm_class(network)
    
    # Only use iterations for RandomAlgorithm
    if isinstance(algorithm, RandomAlgorithm):
        best_quality, best_routes = algorithm.find_best_solution(iterations=iterations or 1000)
    else:
        best_quality, best_routes = algorithm.find_best_solution()
    
    stats = SolutionStatistics(best_quality, best_routes)
    print(f"\nResults for {algorithm_class.__name__}:")
    stats.print_stats()
    

def main():
    parser = argparse.ArgumentParser(description='Run rail network optimization algorithms')
    parser.add_argument('--algorithm', type=str, choices=['random', 'bfs', 'bfs_v2', 'beam', 'beam_v2', 'all'], 
                      default='all', help='Algorithm to run (default: all)')
    parser.add_argument('--iterations', type=int, default=1000,
                      help='Number of iterations for random algorithm (default: 1000)')
    
    args = parser.parse_args()
    
    try:
        # Initialize network
        network = RailNetwork()
        network.load_stations(STATIONS_FILE)
        network.load_connections(CONNECTIONS_FILE)
        
        # Define algorithm mapping
        algorithms = {
            'random': RandomAlgorithm,
            'bfs': SimplifiedBFSAlgorithm,
            'bfs_v2': SimplifiedBFSAlgorithmV2,
            'beam': BeamSearchAlgorithm,
            'beam_v2': BeamSearchAlgorithmV2
        }
        
        if args.algorithm == 'all':
            # Run all algorithms
            for algo_name, algo_class in algorithms.items():
                if algo_name == 'random':
                    iterations = args.iterations
                else:
                    iterations = None
                run_algorithm(algo_class, network, iterations)
        else:
            # Run specific algorithm
            algo_class = algorithms[args.algorithm]
            if args.algorithm == 'random':
                iterations = args.iterations
            else:
                iterations = None
            run_algorithm(algo_class, network, iterations)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Stations file path: {STATIONS_FILE}")
        print(f"Connections file path: {CONNECTIONS_FILE}")
        
if __name__ == "__main__":
    main()