import pandas as pd
import folium

# Bronnen:
# https://python-graph-gallery.com/312-add-markers-on-folium-map/
# https://realpython.com/python-folium-web-maps-from-data/ 

# We halen hier de data op van de coördinaten en de verbindingen van de stations
stations = pd.read_csv('data/StationsHolland.csv', header=None, names=['station', 'y', 'x'], skiprows=1)
connections = pd.read_csv('data/ConnectiesHolland.csv', header=None, names=['station1', 'station2', 'distance'], skiprows=0)

# We maken een dictionary met de coördinaten van elk station gekoppeld aan het bijbehorende station
station_coordinate = {}
for index, row in stations.iterrows():
    station = row['station']
    y_coordinate = row['y']
    x_coordinate = row['x']
    station_coordinate[station] = {'y': y_coordinate, 'x': x_coordinate}

# We creëren een kaart gezoomed op Nederland
m = folium.Map(location=[52.1326, 4.2913], zoom_start=7)

# Voeg markers toe voor de stations
for station, coordinate in station_coordinate.items():
    folium.Marker(
        location=[coordinate['y'], coordinate['x']],
        popup=station,
    ).add_to(m)

# Voeg lijnen toe voor de verbindingen
for _, row in connections.iterrows():
    if row['station1'] in station_coordinate and row['station2'] in station_coordinate:
        folium.PolyLine(
            locations=[
                [station_coordinate[row['station1']]['y'], station_coordinate[row['station1']]['x']],
                [station_coordinate[row['station2']]['y'], station_coordinate[row['station2']]['x']]
            ]
        ).add_to(m)

# we slaan de map op in een html file in de visualization map
m.save("code/visualization/visualisation_map.html")

