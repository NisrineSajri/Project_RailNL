#!/usr/bin/env python3

import os
import sys
import argparse
from typing import Optional

# Voeg de juiste directories toe aan Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from code.classes.rail_network import RailNetwork
from code.classes.solution_statistics import SolutionStatistics
from code.algorithms.random_algorithm import RandomAlgorithm
from code.algorithms.greedy import GreedyAlgorithm
from code.algorithms.beam_greedy import BeamSearchAlgorithm
from code.algorithms.beam_greedy_random import BeamSearchAlgorithmV2
from code.algorithms.beam_heuristics_random import BeamSearchAlgorithmV3
from code.algorithms.hill_climber import HillClimber
from code.algorithms.dijkstra_heuristic import DijkstraHeuristicAlgorithm
from code.algorithms.dijkstra_algorithm import DijkstraAlgorithm
from code.constants import HOLLAND_CONFIG, NATIONAL_CONFIG
from code.experiments.run_experiments import run_algorithm_experiments
from code.experiments.analyze_results import analyze_results, load_algorithm_results

def parse_arguments():
    """Verwerk command line argumenten."""
    parser = argparse.ArgumentParser(description='Rail Netwerk Route Optimalisatie')
    
    # Maak subparsers voor verschillende modi
    subparsers = parser.add_subparsers(dest='mode', help='Operatie modus')
    
    # Parser voor reguliere uitvoering
    run_parser = subparsers.add_parser('run', help='Voer een enkel algoritme uit')
    run_parser.add_argument('--dataset', type=str, choices=['holland', 'national'], 
                           default='holland', help='Dataset om te gebruiken (holland/national)')
    run_parser.add_argument('--algorithm', type=str, 
                           choices=['random', 'greedy', 'beam_greedy', 'beam_greedy_random',
                                   'beam_heuristics_random', 'hill_climber', 'dijkstra_heuristic', 'dijkstra'],
                           default='random', help='Algoritme om te gebruiken voor optimalisatie')
    run_parser.add_argument('--iterations', type=int, default=1000,
                           help='Aantal iteraties voor toepasselijke algoritmes')
    
    # Parser voor experiment modus
    exp_parser = subparsers.add_parser('experiment', help='Voer experimenten uit')
    exp_parser.add_argument('--algorithm', type=str, 
                           choices=['random', 'greedy', 'beam_greedy', 'beam_greedy_random',
                                   'beam_heuristics_random', 'hill_climber', 'dijkstra_heuristic', 'dijkstra', 'all'],
                           default='all', help='Algoritme om te experimenteren')
    exp_parser.add_argument('--dataset', type=str, choices=['holland', 'national', 'both'],
                           default='both', help='Dataset voor experimenten')
    exp_parser.add_argument('--total-time', type=int, default=3600,
                           help='Totale tijd in seconden om experimenten uit te voeren')
    exp_parser.add_argument('--run-time', type=int, default=60,
                           help='Tijdslimiet in seconden voor elke run')
    
    # Parser voor analyse modus
    analysis_parser = subparsers.add_parser('analyze', help='Analyseer experiment resultaten')
    
    return parser.parse_args()

def create_algorithm(name: str, network: RailNetwork, config: dict):
    """
    Maak een instantie van het gekozen algoritme.
    
    Args:
        name: Naam van het te gebruiken algoritme
        network: Het railnetwerk om mee te werken
        config: Configuratie met tijdslimiet en maximum aantal routes
        
    Returns:
        Een instantie van het gekozen algoritme
    """
    algorithms = {
        'random': RandomAlgorithm,
        'greedy': GreedyAlgorithm,
        'beam_greedy': BeamSearchAlgorithm,
        'beam_greedy_random': BeamSearchAlgorithmV2,
        'beam_heuristics_random': BeamSearchAlgorithmV3,
        'hill_climber': HillClimber,
        'dijkstra_heuristic': DijkstraHeuristicAlgorithm,
        'dijkstra': DijkstraAlgorithm
    }
    
    if name not in algorithms:
        raise ValueError(f"Onbekend algoritme: {name}")
        
    return algorithms[name](network, time_limit=config['time_limit'], 
                          max_routes=config['max_routes'])

def run_algorithm(args) -> None:
    """
    Voer een enkel algoritme uit met de opgegeven parameters.
    
    Args:
        args: Command line argumenten
    """
    # Kies de juiste configuratie
    config = NATIONAL_CONFIG if args.dataset == 'national' else HOLLAND_CONFIG
    
    # Initialiseer het netwerk
    network = RailNetwork()
    
    # Laad de data
    network.load_stations(config['stations_file'])
    network.load_connections(config['connections_file'])
    
    # Maak en voer het algoritme uit
    algorithm = create_algorithm(args.algorithm, network, config)
    quality, routes = algorithm.find_best_solution(args.iterations)
    
    # Maak en toon statistieken
    stats = SolutionStatistics(quality, routes, network)
    stats.print_stats()

def run_experiments(args) -> None:
    """
    Voer experimenten uit met de opgegeven parameters.
    
    Args:
        args: Command line argumenten
    """
    if args.algorithm == 'all':
        algorithms = ['random', 'greedy', 'beam_greedy', 'beam_greedy_random',
                     'beam_heuristics_random', 'hill_climber', 'dijkstra_heuristic', 'dijkstra']
    else:
        algorithms = [args.algorithm]
    
    if args.dataset == 'both':
        datasets = ['holland', 'national']
    else:
        datasets = [args.dataset]
    
    for algorithm in algorithms:
        for dataset in datasets:
            print(f"\nStart experimenten voor {algorithm} op {dataset} dataset...")
            run_algorithm_experiments(algorithm, dataset, args.total_time, args.run_time)

def analyze_experiment_results(args) -> None:
    """
    Analyseer en visualiseer experiment resultaten.
    
    Args:
        args: Command line argumenten
    """
    # Verkrijg paden relatief aan dit script
    experiments_dir = os.path.join(current_dir, 'code', 'experiments')
    results_dir = os.path.join(experiments_dir, 'results')
    visualization_dir = os.path.join(current_dir, 'visualization')
    
    # Laad en analyseer resultaten
    results = load_algorithm_results(results_dir)
    analyze_results(results, visualization_dir)
    print("Analyse voltooid. Resultaten opgeslagen in visualisatie directory.")

def main():
    """
    Hoofdfunctie voor het uitvoeren van de rail netwerk optimalisatie.
    Verwerkt command-line argumenten en voert de gekozen operatie modus uit.
    """
    args = parse_arguments()
    
    if args.mode == 'run':
        run_algorithm(args)
    elif args.mode == 'experiment':
        run_experiments(args)
    elif args.mode == 'analyze':
        analyze_experiment_results(args)
    else:
        print("Specificeer een modus: run, experiment, of analyze")
        sys.exit(1)

if __name__ == "__main__":
    main()