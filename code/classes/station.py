class Station:
    def __init__(self, name, x, y):
        """
        Initialiseer een Station object.

        Argumenten:
            name (str): De naam van het station.
            x (float): De x-coördinaat van het station.
            y (float): De y-coördinaat van het station.
        """
        self.name = name
        self.x = x
        self.y = y
        self.connections = {}  # station_name -> Verbinding

    def add_connection(self, connection):
        """
        Voeg een verbinding toe aan dit station.

        Argumenten:
            connection (Connection): Het verbindingsobject dat moet worden toegevoegd aan het station.
        """
        destination = connection.get_other_station(self.name)
        self.connections[destination] = connection

    def get_possible_destinations(self):
        """
        Verkrijg alle mogelijke bestemmingen vanaf dit station.

        Retour:
            list: Een lijst van stationnamen die als bestemmingen vanuit dit station beschikbaar zijn.
        """
        return list(self.connections.keys())

    def __str__(self):
        """
        Geeft een stringrepresentatie van het Station.

        Retour:
            str: Een string die de naam en coördinaten van het station weergeeft.
        """
        return f"Station({self.name}, x={self.x}, y={self.y})"
