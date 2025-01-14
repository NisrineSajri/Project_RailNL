
import random
from typing import List, Tuple
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from classes.rail_network import RailNetwork
from classes.route import Route


# we gaan een graph creëren ("A": {"B": 4, "C": 3})
graph = {}
for index, row in connections.iterrows():
    station_begin = row['station1']
    station_end = row['station2']
    dist = row['distance']
    
    # als de key nog niet in graph staat
    if station_begin not in graph[0]:
        graph[station_begin] = {station_end: dist}

    # als de key wel al bestaat, moeten we geen nieuwe key toevoegen, maar alleen values toevoegen aan juiste key
    else:
        # voeg values toe aan bestaande key

    # we doen hetzelfde maar dan van eindstation naar beginstation
    if station_end not in graph[0]:
        graph[station_end] = {station_begin: dist}
    else:
        # voeg values toe aan bestaande key
