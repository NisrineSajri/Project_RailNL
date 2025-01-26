import argparse
from typing import List, Type
import os
import sys

# Voeg de bovenliggende directory toe aan de Python path
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
from algorithms.hill_climber import HillClimber
from algorithms.beam_search_v3 import HeuristicRandomBFS
from constants import HOLLAND_CONFIG, NATIONAL_CONFIG

def run_algorithm(algorithm_class, network: RailNetwork, config: dict, iterations: int = None) -> None:
    """
    Voer het opgegeven algoritme uit en druk de resultaten af.
    
    Argumenten:
        algorithm_class: Klasse van het algoritme om uit te voeren
        network: RailNetwork instantie
        config: Configuratie dictionary met max_routes en time_limit
        iterations: Aantal iteraties (alleen gebruikt voor RandomAlgorithm)
    """
    # Initialiseer het algoritme met dataset-specifieke parameters
    algorithm = algorithm_class(
        network, 
        time_limit=config['time_limit'], 
        max_routes=config['max_routes']
    )
    
    # Gebruik alleen iteraties voor RandomAlgorithm
    if isinstance(algorithm, RandomAlgorithm):
        best_quality, best_routes = algorithm.find_best_solution(iterations=iterations or 1000)
    else:
        best_quality, best_routes = algorithm.find_best_solution()
    
    stats = SolutionStatistics(best_quality, best_routes, network)
    print(f"\nResults for {algorithm_class.__name__}:")
    stats.print_stats()

def main():
    parser = argparse.ArgumentParser(description='Run rail network optimization algorithms')
    parser.add_argument('--algorithm', type=str, 
                      choices=['random', 'bfs', 'bfs_v2', 'beam', 'beam_v2', 'beam_v3', 'dijkstra', 'greedy', 'hill', 'all'], 
                      default='all', help='Algorithm to run (default: all)')
    parser.add_argument('--iterations', type=int, default=1000,
                      help='Number of iterations for random algorithm (default: 1000)')
    parser.add_argument('--dataset', type=str, choices=['holland', 'national'],
                      default='holland', help='Dataset to use (default: holland)')
    
    args = parser.parse_args()
    
    try:
        # Selecteer configuratie op basis van dataset
        config = HOLLAND_CONFIG if args.dataset == 'holland' else NATIONAL_CONFIG
        
        # Initialiseer netwerk
        network = RailNetwork()
        network.load_stations(config['stations_file'])
        network.load_connections(config['connections_file'])
        
        # Initialiseer netwerk
        algorithms = {
            'random': RandomAlgorithm,
            'bfs': SimplifiedBFSAlgorithm,
            'bfs_v2': SimplifiedBFSAlgorithmV2,
            'beam': BeamSearchAlgorithm,
            'beam_v2': BeamSearchAlgorithmV2,
            'beam_v3': HeuristicRandomBFS,
            'dijkstra': DijkstraAlgorithm,
            'greedy': GreedyAlgorithm,
            'hill': HillClimber
        }
        
        if args.algorithm == 'all':
            # Voer alle algoritmen uit
            for algo_name, algo_class in algorithms.items():
                if algo_name == 'random':
                    iterations = args.iterations
                else:
                    iterations = None
                run_algorithm(algo_class, network, config, iterations)
        else:
            # Voer specifiek algoritme uit
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