import pytest
from classes.route import Route
from classes.connection import Connection

@pytest.fixture
def sample_route():
    """Create a sample route for testing"""
    return Route(time_limit=120)

@pytest.fixture
def sample_connection():
    """Create a sample connection for testing"""
    return Connection("Amsterdam", "Rotterdam", 40)

def test_route_initialization(sample_route):
    """Test route initialization"""
    assert sample_route.stations == []
    assert sample_route.total_time == 0
    assert len(sample_route.connections_used) == 0
    assert sample_route.time_limit == 120

def test_add_connection_success(sample_route, sample_connection):
    """Test adding a valid connection"""
    assert sample_route.add_connection(sample_connection) == True
    assert len(sample_route.stations) == 2
    assert sample_route.total_time == 40
    assert len(sample_route.connections_used) == 1

def test_add_connection_exceeds_time_limit(sample_route):
    """Test adding a connection that would exceed time limit"""
    long_connection = Connection("Amsterdam", "Groningen", 150)
    assert sample_route.add_connection(long_connection) == False
    assert len(sample_route.stations) == 0
    assert sample_route.total_time == 0

def test_multiple_connections(sample_route):
    """Test adding multiple connections"""
    conn1 = Connection("Amsterdam", "Utrecht", 20)
    conn2 = Connection("Utrecht", "Den Haag", 30)
    
    sample_route.add_connection(conn1)
    sample_route.add_connection(conn2)
    
    assert len(sample_route.stations) == 3
    assert sample_route.total_time == 50
    assert len(sample_route.connections_used) == 2
    assert sample_route.stations == ["Amsterdam", "Utrecht", "Den Haag"]

def test_connection_marking_as_used(sample_route, sample_connection):
    """Test that connections are marked as used when added"""
    assert not sample_connection.used
    sample_route.add_connection(sample_connection)
    assert sample_connection.used