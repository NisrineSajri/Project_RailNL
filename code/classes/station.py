class Station:
    def __init__(self, name, x, y):
        """
        Initialize a Station object.
        """
        self.name = name
        self.x = x
        self.y = y
        self.connections = {}  # station_name -> Connection

    def add_connection(self, connection):
        """
        Add a connection to this station.
        """
        destination = connection.get_other_station(self.name)
        self.connections[destination] = connection

    def get_possible_destinations(self):
        """
        Get all possible destinations from this station.
        """
        return list(self.connections.keys())

    def __str__(self):
        """
        String representation of the Station.
        """
        return f"Station({self.name}, x={self.x}, y={self.y})"