import os

# Get the absolute path to the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths
DATA_DIR = os.path.join(ROOT_DIR, "data")
STATIONS_FILE = os.path.join(DATA_DIR, "StationsNationaal.csv")
CONNECTIONS_FILE = os.path.join(DATA_DIR, "ConnectiesNationaal.csv")

""