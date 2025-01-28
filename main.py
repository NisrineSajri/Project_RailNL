#!/usr/bin/env python3

import os
import sys
import argparse

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
from code.algorithms.a_star_algorithm import AStarAlgorithm
from code.algorithms.dijkstra_algorithm import DijkstraAlgorithm
from code.constants import HOLLAND_CONFIG, NATIONAL_CONFIG

def parse_arguments():
    """Verwerk command line argumenten."""
    parser = argparse.ArgumentParser(description='Rail Netwerk Route Optimalisatie')
    
    parser.add_argument('--dataset', type=str, choices=['holland', 'national'], 
                       default='holland', help='Dataset om te gebruiken (holland/national)')
    
    parser.add_argument('--algorithm', type=str, 
                       choices=['random', 'greedy', 'beam_greedy', 'beam_greedy_random',
                               'beam_heuristics_random', 'hill_climber', 'a_star', 'dijkstra'],
                       default='random', help='Algoritme om te gebruiken voor optimalisatie')
    
    parser.add_argument('--iterations', type=int, default=1000,
                       help='Aantal iteraties voor toepasselijke algoritmes')
    
    return parser.parse_args()

def create_algorithm(name, network, config):
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
        'a_star': AStarAlgorithm,
        'dijkstra': DijkstraAlgorithm
    }
    
    if name not in algorithms:
        raise ValueError(f"Onbekend algoritme: {name}")
        
    return algorithms[name](network, time_limit=config['time_limit'], 
                          max_routes=config['max_routes'])

def main():
    """
    Hoofdfunctie voor het uitvoeren van de rail netwerk optimalisatie.
    Verwerkt command-line argumenten en voert het gekozen algoritme uit.
    """
    args = parse_arguments()
    
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
    
if __name__ == "__main__":
    main()