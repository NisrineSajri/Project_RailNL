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
from algorithms.dijkstra_algorithm import DijkstraAlgorithm
from algorithms.greedy import GreedyAlgorithm
from constants import HOLLAND_CONFIG, NATIONAL_CONFIG

def run_algorithm(algorithm_class, network: RailNetwork, config: dict, iterations: int = None) -> None:
    """
    Run the specified algorithm and print its results.
    
    Args:
        algorithm_class: Class of the algorithm to run
        network: RailNetwork instance
        config: Configuration dictionary containing max_routes and time_limit
        iterations: Number of iterations (only used for RandomAlgorithm)
    """
    # Initialize algorithm with dataset-specific parameters
    algorithm = algorithm_class(
        network, 
        time_limit=config['time_limit'], 
        max_routes=config['max_routes']
    )
    
    # Only use iterations for RandomAlgorithm
    if isinstance(algorithm, RandomAlgorithm):
        best_quality, best_routes = algorithm.find_best_solution(iterations=iterations or 1000)
    else:
        best_quality, best_routes = algorithm.find_best_solution()
    
    stats = SolutionStatistics(best_quality, best_routes)
    print(f"\nResults for {algorithm_class.__name__}:")
    stats.print_stats()

# Bron: https://www.tutorialspoint.com/how-to-save-a-python-dictionary-to-csv-file
def run_visualization(self):
    # Specify the CSV file name
    csv_file = 'visualization_algorithms.csv'

    # Writing to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'Value'])
        
        # Write data
        for key, value in my_dict.items():
            writer.writerow([key, value])

    print(f"Dictionary saved to {csv_file}")
        

def main():
    parser = argparse.ArgumentParser(description='Run rail network optimization algorithms')
    parser.add_argument('--algorithm', type=str, 
                      choices=['random', 'bfs', 'bfs_v2', 'beam', 'beam_v2', 'dijkstra', 'greedy', 'all'], 
                      default='all', help='Algorithm to run (default: all)')
    parser.add_argument('--iterations', type=int, default=1000,
                      help='Number of iterations for random algorithm (default: 1000)')
    parser.add_argument('--dataset', type=str, choices=['holland', 'national'],
                      default='holland', help='Dataset to use (default: holland)')
    
    args = parser.parse_args()
    
    try:
        # Select configuration based on dataset
        config = HOLLAND_CONFIG if args.dataset == 'holland' else NATIONAL_CONFIG
        
        # Initialize network
        network = RailNetwork()
        network.load_stations(config['stations_file'])
        network.load_connections(config['connections_file'])
        
        # Define algorithm mapping
        algorithms = {
            'random': RandomAlgorithm,
            'bfs': SimplifiedBFSAlgorithm,
            'bfs_v2': SimplifiedBFSAlgorithmV2,
            'beam': BeamSearchAlgorithm,
            'beam_v2': BeamSearchAlgorithmV2,
            'dijkstra': DijkstraAlgorithm,
            'greedy': GreedyAlgorithm
        }
        
        if args.algorithm == 'all':
            # Run all algorithms
            for algo_name, algo_class in algorithms.items():
                if algo_name == 'random':
                    iterations = args.iterations
                else:
                    iterations = None
                run_algorithm(algo_class, network, config, iterations)
        else:
            # Run specific algorithm
            algo_class = algorithms[args.algorithm]
            if args.algorithm == 'random':
                iterations = args.iterations
            else:
                iterations = None
            run_algorithm(algo_class, network, config, iterations)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Config being used: {config}")
        
if __name__ == "__main__":
    main()