import pytest
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.connection import Connection
from classes.station import Station
from constants import HOLLAND_CONFIG

@pytest.fixture
def sample_network():
    """Create a sample network for testing"""
    network = RailNetwork()
    network.load_stations(HOLLAND_CONFIG['stations_file'])
    network.load_connections(HOLLAND_CONFIG['connections_file'])
    return network

def test_network_initialization(sample_network):
    """Test network initialization and loading"""
    assert len(sample_network.stations) > 0
    assert len(sample_network.connections) > 0
    assert len(sample_network.routes) == 0

def test_calculate_quality():
    """Test quality calculation with known values"""
    network = RailNetwork()
    
    # Create a simple network with 2 connections
    conn1 = Connection("A", "B", 30)
    conn2 = Connection("B", "C", 40)
    network.connections = [conn1, conn2]
    
    # Create a route that uses one connection
    route = Route()
    route.add_connection(conn1)
    network.routes.append(route)
    
    # Calculate quality: p=0.5, T=1, Min=30
    # K = 0.5*10000 - (1*100 + 30) = 4870
    quality = network.calculate_quality()
    assert quality == 4870

def test_get_used_connections(sample_network):
    """Test getting used connections"""
    # Create and add a route
    route = Route()
    connection = sample_network.connections[0]
    route.add_connection(connection)
    sample_network.routes.append(route)
    
    used_connections = sample_network.get_used_connections()
    assert len(used_connections) == 1
    assert connection in used_connections

def test_reset_network(sample_network):
    """Test network reset functionality"""
    # Add a route and mark some connections as used
    route = Route()
    connection = sample_network.connections[0]
    route.add_connection(connection)
    sample_network.routes.append(route)
    
    # Reset network
    sample_network.reset()
    
    assert len(sample_network.routes) == 0
    assert not any(conn.used for conn in sample_network.connections)

def test_network_constraints():
    """Test that network respects time and route constraints"""
    network = RailNetwork()
    
    # Add some sample connections to the network
    conn1 = Connection("Amsterdam", "Rotterdam", 40)
    conn2 = Connection("Rotterdam", "Den Haag", 30)
    network.connections = [conn1, conn2]
    
    # Add the connections to stations
    network.stations["Amsterdam"] = Station("Amsterdam", 0, 0)
    network.stations["Rotterdam"] = Station("Rotterdam", 1, 1)
    network.stations["Den Haag"] = Station("Den Haag", 2, 2)
    
    network.stations["Amsterdam"].add_connection(conn1)
    network.stations["Rotterdam"].add_connection(conn1)
    network.stations["Rotterdam"].add_connection(conn2)
    network.stations["Den Haag"].add_connection(conn2)
    
    # Create routes that exceed Holland config constraints (max 7 routes)
    for _ in range(8):
        route = Route()
        route.add_connection(conn1)  # Add actual connection to route
        network.routes.append(route)
    
    quality = network.calculate_quality()
    
    # Verify constraints
    assert len(network.routes) > HOLLAND_CONFIG['max_routes']  # Exceeds max routes
    
    # Verify route time constraints
    for route in network.routes:
        assert route.total_time <= HOLLAND_CONFIG['time_limit']