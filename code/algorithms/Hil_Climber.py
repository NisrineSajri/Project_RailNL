import random
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route
from greedy import GreedyAlgorithm
from constants import HOLLAND_CONFIG, NATIONAL_CONFIG
from classes.station import Station


class HillClimberAlgorithm:
    def __init__(self, network: RailNetwork):
        """
        Initialize the HillClimber class.
        Args:
            network (RailNetwork): The rail network of stations and connections.
        """
        self.network = network
        self.best_solution = None
        self.best_quality = 0

    def generate_initial_solution(self):
        """
        Generate an initial solution using the Greedy algorithm.
        """
        greedy = GreedyAlgorithm(self.network)
        quality = greedy.runGreedy()  # Get the greedy solution's total quality
        self.best_solution = list(self.network.routes)  # Save the greedy routes
        self.best_quality = quality

    def evaluate_solution(self) -> float:
        """
        Evaluate the quality of the current solution.
        Returns:
            float: The quality of the solution (time).
        """
        return self.network.calculate_quality()  # Implement your quality evaluation function



