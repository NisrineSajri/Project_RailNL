import os

# Get the absolute path to the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Dataset configurations
HOLLAND_CONFIG = {
    'stations_file': os.path.join(DATA_DIR, "StationsHolland.csv"),
    'connections_file': os.path.join(DATA_DIR, "ConnectiesHolland.csv"),
    'max_routes': 7,
    'time_limit': 120
}

NATIONAL_CONFIG = {
    'stations_file': os.path.join(DATA_DIR, "StationsNationaal.csv"),
    'connections_file': os.path.join(DATA_DIR, "ConnectiesNationaal.csv"),
    'max_routes': 20,
    'time_limit': 180
}