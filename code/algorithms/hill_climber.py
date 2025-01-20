# https://www.geeksforgeeks.org/introduction-hill-climbing-artificial-intelligence/?utm_source=chatgpt.com#pseudocode-of-hill-climbing-algorithm

import random

from copy import deepcopy
from typing import List, Tuple
from classes.rail_network import RailNetwork
from classes.route import Route
from algorithms.greedy import GreedyAlgorithm


class HillClimber:
    def __init__(self, network: RailNetwork, initial_routes: List[Route] = None, time_limit: int = 120, max_routes: int = 7):
        """
        Initialiseer de HillClimber met een initiële oplossing (greedy algoritme)
        Args:
            network: Het spoornetwerk om mee te werken
            max_routes: Maximaal aantal routes
            time_limit: Maximale tijdslimiet voor routes in minuten
            current_routes: de initiële oplossing 
        """
        self.network = network
        self.max_routes = max_routes
        self.max_time = time_limit

        # Als geen initiële oplossing wordt gegeven, gebruik GreedyAlgorithm 
        # (of andere algorithm, morgen vragen)
        if initial_routes is None:
            # Reset network state before getting initial solution
            for conn in self.network.connections:
                conn.used = False
            self.network.routes.clear()
            
            greedy = GreedyAlgorithm(network, time_limit=time_limit, max_routes=max_routes)
            _, best_routes = greedy.find_best_solution()
            if best_routes:  # Only initialize with best_routes if they exist
                self.current_routes = self.copy_routes(best_routes)
            else:
                # Create at least one initial route
                initial_route = Route(time_limit=self.max_time)
                first_station = next(iter(network.stations))
                initial_route.stations = [first_station]
                self.current_routes = [initial_route]

    def copy_routes(self, routes: List[Route]) -> List[Route]:
        """Maak een diepe kopie van routes om de originele routes niet te wijzigen."""
        return deepcopy(routes)

    def modify_route(self, route: Route) -> Route:
        """
        Maak een kleine aanpassing aan een route.
        Mogelijke aanpassingen (random):
        1. Verwijder laatste verbinding (dus de één na laatste en laatste halte weg) en probeer een ander pad
        2. Verwijder willekeurige verbinding en herbouw vanaf dat punt
        3. Begin vanaf een ander station in de route
        """
        new_route = Route(time_limit=self.max_time)
        optie = random.choice([1, 2, 3])
            
        # Kies een startpunt gebaseerd op optie type (random keuze)
        
        # Verwijder laatste verbinding
        if optie == 1:
            # ckeck of de route meer dan 2 stations bevat
            if len(route.stations) > 2:
                # Kies dan de op één na laatste station als startpunt
                start_idx = len(route.stations) - 2
                # We zoeken naar connecties vanaf dat punt
                start_station = route.stations[start_idx]
            else:
                # Als er maar 2 of minder stations zijn, kies het eerste station als startpunt
                start_station = route.stations[0]
        
        # Verwijder willekeurige verbinding
        elif optie == 2:
            # Controleer of de route meer dan 2 stations bevat
            if len(route.stations) > 2:
                # Kies willekeurig een station tot het op één na laatste station
                start_station = random.choice(route.stations[:-1])
            else:
                # Als er maar 2 of minder stations zijn, kies het eerste station als startpunt
                start_station = route.stations[0]

        # Begin vanaf een ander station in de route
        elif optie == 3: 
            # Kies willekeurig een station uit de route als startpunt
            start_station = random.choice(route.stations)

        # Maak een nieuwe route vanaf het gekozen startstation (create_route() van greedy gebruikt)
        greedy_algorithm = GreedyAlgorithm(self.network, time_limit=self.max_time)

        # Creëer de route vanuit het gekozen startstation
        new_route = greedy_algorithm.create_route(self.network.stations[start_station])
        
        if not new_route.stations:
            new_route.stations = [start_station]
            
        return new_route 
    
    def find_best_solution(self, iterations: int = 1000) -> Tuple[float, List[Route]]:
        """
        Voer hill climbing algoritme uit om een betere oplossing te vinden.

        Args:
            iterations: Aantal iteraties om uit te voeren

        Returns:
            Tuple[float, List[Route]]: Beste kwaliteitsscore en bijbehorende routes
        """
        # Reset network state
        for conn in self.network.connections:
            conn.used = False
        self.network.routes.clear()
        
        if not self.current_routes:
            return 0, []
            
        best_quality = self.network.calculate_quality()
        best_routes = self.copy_routes(self.current_routes)
        
        i = 0
        while i < iterations:
            try:
                # Kies willekeurige route om aan te passen
                route = random.choice(self.current_routes)

                # Bewaar huidige staat
                old_route = route
                # zet die verbinding op unused om zo een andere verbinding te maken en die te kunnen grbuiken als nodig
                for conn in old_route.connections_used:
                    conn.used = False
                # Probeer aanpassing
                new_route = self.modify_route(old_route)
                # Zoek de index van de route in de lijst en vervang [route1, route2, route3]
                route_idx = self.current_routes.index(old_route)
                self.current_routes[route_idx] = new_route # dus [route1, new_route, route3]

                # Bereken nieuwe kwaliteit
                new_quality = self.network.calculate_quality()

                # Accepteer als beter, anders terugdraaien
                if new_quality > best_quality:
                    best_quality = new_quality
                    best_routes = self.copy_routes(self.current_routes)
                else:
                    # Zet oude route terug
                    self.current_routes[route_idx] = old_route
                    for conn in old_route.connections_used:
                        conn.used = True
                
                # Verhoog de teller voor de volgende iteratie
                i += 1
            except Exception:
                break
                
        return best_quality, best_routes

    def find_single_solution(self) -> Tuple[float, List[Route]]:
        """
        Find best solution (single iteration since deterministic).
            
        Returns:
            Tuple[float, List[Route]]: Quality score and corresponding routes
        """
        # Bereken de huidige kwaliteit van het netwerk
        quality = self.network.calculate_quality()
        
        # Maak een diepe kopie van de huidige routes
        best_routes = [Route() for _ in self.current_routes]
        for new_route, old_route in zip(best_routes, self.current_routes):
            new_route.stations = old_route.stations.copy()
            new_route.total_time = old_route.total_time
            new_route.connections_used = old_route.connections_used.copy()
        
        # Geef de huidige kwaliteit en routes terug
        return quality, best_routes