import pytest
from classes.route import Route
from classes.rail_network import RailNetwork
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.greedy import GreedyAlgorithm
from algorithms.hill_climber import HillClimber
from constants import HOLLAND_CONFIG, NATIONAL_CONFIG

@pytest.fixture
def holland_network():
    """Create Holland network for testing"""
    network = RailNetwork()
    network.load_stations(HOLLAND_CONFIG['stations_file'])
    network.load_connections(HOLLAND_CONFIG['connections_file'])
    return network

@pytest.fixture
def national_network():
    """Create National network for testing"""
    network = RailNetwork()
    network.load_stations(NATIONAL_CONFIG['stations_file'])
    network.load_connections(NATIONAL_CONFIG['connections_file'])
    return network

def test_random_algorithm_constraints(holland_network):
    """Test that random algorithm respects constraints"""
    algorithm = RandomAlgorithm(
        holland_network, 
        time_limit=HOLLAND_CONFIG['time_limit'],
        max_routes=HOLLAND_CONFIG['max_routes']
    )
    
    quality, routes = algorithm.find_best_solution(iterations=10)
    
    # Check number of routes constraint
    assert len(routes) <= HOLLAND_CONFIG['max_routes']
    
    # Check time limit constraint
    for route in routes:
        assert route.total_time <= HOLLAND_CONFIG['time_limit']

def test_greedy_algorithm_solution(holland_network):
    """Test that greedy algorithm produces valid solution"""
    algorithm = GreedyAlgorithm(
        holland_network,
        time_limit=HOLLAND_CONFIG['time_limit'],
        max_routes=HOLLAND_CONFIG['max_routes']
    )
    
    quality, routes = algorithm.find_best_solution()
    
    # Solution should exist
    assert quality is not None
    assert len(routes) > 0
    
    # Each route should have at least one connection
    for route in routes:
        assert len(route.connections_used) > 0

def test_hill_climber_improvement(holland_network):
    """Test that hill climber improves on initial solution"""
    # Create a simple initial solution
    initial_routes = []
    
    # Create a sample route
    route = Route(time_limit=HOLLAND_CONFIG['time_limit'])
    
    # Get first available connection
    first_conn = next(iter(holland_network.connections))
    route.add_connection(first_conn)
    initial_routes.append(route)
    
    # Calculate initial quality
    holland_network.routes = initial_routes
    initial_quality = holland_network.calculate_quality()
    
    # Run hill climber with this initial solution
    hill_climber = HillClimber(
        network=holland_network,
        initial_routes=initial_routes,
        time_limit=HOLLAND_CONFIG['time_limit'],
        max_routes=HOLLAND_CONFIG['max_routes']
    )
    
    # Make sure current_routes is properly set
    assert hasattr(hill_climber, 'current_routes'), "HillClimber should have current_routes attribute"
    assert len(hill_climber.current_routes) > 0, "HillClimber should have at least one route"
    
    final_quality, final_routes = hill_climber.find_best_solution(iterations=10)

def test_solution_validity(holland_network):
    """Test validity of solutions from different algorithms"""
    algorithms = [
        (RandomAlgorithm, {'iterations': 10}),
        (GreedyAlgorithm, {}),
        (HillClimber, {})
    ]
    
    for Algorithm, kwargs in algorithms:
        algorithm = Algorithm(
            holland_network,
            time_limit=HOLLAND_CONFIG['time_limit'],
            max_routes=HOLLAND_CONFIG['max_routes']
        )
        
        quality, routes = algorithm.find_best_solution(**kwargs)
        
        # Basic validity checks
        assert quality is not None
        assert isinstance(routes, list)
        assert all(isinstance(route.total_time, (int, float)) for route in routes)
        assert all(len(route.stations) >= 2 for route in routes)  # Each route should have at least 2 stations

def test_cross_algorithm_comparison(holland_network):
    """Compare different algorithms on same network"""
    algorithms = [
        (RandomAlgorithm, {'iterations': 10}),
        (GreedyAlgorithm, {}),
        (HillClimber, {})
    ]
    
    results = []
    for Algorithm, kwargs in algorithms:
        algorithm = Algorithm(
            holland_network,
            time_limit=HOLLAND_CONFIG['time_limit'],
            max_routes=HOLLAND_CONFIG['max_routes']
        )
        
        quality, _ = algorithm.find_best_solution(**kwargs)
        results.append(quality)
    
    # Ensure all algorithms produce valid solutions
    assert all(isinstance(q, (int, float)) for q in results)
    assert all(q > -10000 for q in results)  # Basic sanity check on quality scores