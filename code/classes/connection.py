class Connection:
    def __init__(self, station1: str, station2: str, distance: int):
        """
        Initialize a Connection object.
        
        Args:
            station1 (str): Name of the first station
            station2 (str): Name of the second station
            distance (int): Distance/time between stations in minutes
        """
        self.station1 = station1
        self.station2 = station2
        self.distance = distance
        self.used = False

    def get_other_station(self, station: str) -> str:
        """
        Get the name of the station at the other end of the connection.
        
        Args:
            station (str): Name of one station in the connection
            
        Returns:
            str: Name of the other station
        """
        if station == self.station1:
            return self.station2
        else:
            return self.station1

    def __str__(self) -> str:
        """
        String representation of the Connection.
        
        Returns:
            str: String describing the connection
        """
        return f"Connection({self.station1} - {self.station2}, {self.distance} min)"