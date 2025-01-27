import pytest
from classes.rail_network import RailNetwork
from classes.route import Route
from classes.connection import Connection
from classes.station import Station
from classes.solution_statistics import SolutionStatistics

@pytest.fixture
def sample_network():
    """Maak een eenvoudig testnetwerk met drie stations en twee verbindingen"""
    network = RailNetwork()
    
    # Maak teststations aan
    station_a = Station("A", 0, 0)
    station_b = Station("B", 1, 0)
    station_c = Station("C", 2, 0)
    
    network.stations = {
        "A": station_a,
        "B": station_b,
        "C": station_c
    }
    
    # Maak testverbindingen aan
    connection_ab = Connection("A", "B", 10)
    connection_bc = Connection("B", "C", 15)
    
    # Voeg verbindingen toe aan stations
    station_a.add_connection(connection_ab)
    station_b.add_connection(connection_ab)
    station_b.add_connection(connection_bc)
    station_c.add_connection(connection_bc)
    
    # Voeg verbindingen toe aan netwerk
    network.connections = [connection_ab, connection_bc]
    
    return network

def test_solution_statistics_coverage_empty(sample_network):
    """Test dekkingsberekening met lege routes"""
    stats = SolutionStatistics(0, [], sample_network)
    assert stats.get_coverage_percentage() == 0.0
    assert stats.total_connections == 0

def test_solution_statistics_single_route(sample_network):
    """Test dekkingsberekening met één route die één verbinding gebruikt"""
    # Maak een route met één verbinding
    route = Route()
    connection = sample_network.connections[0]  # A-B verbinding
    route.stations = ["A", "B"]
    route.connections_used.add(connection)
    
    stats = SolutionStatistics(0, [route], sample_network)
    
    # Verwachte dekking: 1 gebruikte verbinding / 2 totale verbindingen = 50%
    assert stats.get_coverage_percentage() == 50.0
    assert stats.total_connections == 1

def test_solution_statistics_duplicate_connections(sample_network):
    """Test dekkingsberekening met dezelfde verbinding in meerdere routes"""
    connection = sample_network.connections[0]  # A-B verbinding
    
    # Maak twee routes met dezelfde verbinding
    route1 = Route()
    route1.stations = ["A", "B"]
    route1.connections_used.add(connection)
    
    route2 = Route()
    route2.stations = ["A", "B"]
    route2.connections_used.add(connection)
    
    stats = SolutionStatistics(0, [route1, route2], sample_network)
    
    # Moet nog steeds 50% zijn omdat dezelfde verbinding wordt gebruikt
    assert stats.get_coverage_percentage() == 50.0
    assert stats.total_connections == 1

def test_solution_statistics_full_coverage(sample_network):
    """Test dekkingsberekening met alle verbindingen gebruikt"""
    # Maak een route die alle verbindingen gebruikt
    route = Route()
    route.stations = ["A", "B", "C"]
    route.connections_used.update(sample_network.connections)
    
    stats = SolutionStatistics(0, [route], sample_network)
    
    # Moet 100% zijn omdat alle verbindingen worden gebruikt
    assert stats.get_coverage_percentage() == 100.0
    assert stats.total_connections == 2

def test_solution_statistics_multiple_routes_unique_connections(sample_network):
    """Test dekkingsberekening met meerdere routes met verschillende verbindingen"""
    # Route 1: A -> B
    route1 = Route()
    route1.stations = ["A", "B"]
    route1.connections_used.add(sample_network.connections[0])
    
    # Route 2: B -> C
    route2 = Route()
    route2.stations = ["B", "C"]
    route2.connections_used.add(sample_network.connections[1])
    
    stats = SolutionStatistics(0, [route1, route2], sample_network)
    
    # Moet 100% zijn omdat alle verbindingen worden gebruikt via verschillende routes
    assert stats.get_coverage_percentage() == 100.0
    assert stats.total_connections == 2

def test_total_connections_initialization(sample_network):
    """Test of total_connections correct wordt geïnitialiseerd in SolutionStatistics"""
    # Maak routes met overlappende verbindingen
    connection_ab = sample_network.connections[0]
    
    route1 = Route()
    route1.stations = ["A", "B"]
    route1.connections_used.add(connection_ab)
    
    route2 = Route()
    route2.stations = ["A", "B"]
    route2.connections_used.add(connection_ab)
    
    stats = SolutionStatistics(0, [route1, route2], sample_network)
    
    # Moet 1 zijn, niet 2, omdat dezelfde verbinding in beide routes zit
    assert stats.total_connections == 1