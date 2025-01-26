class Connection:
    def __init__(self, station1: str, station2: str, distance: int):
        """
        Initialiseer een Connection object.
        
        Args:
            station1 (str): Naam van het eerste station
            station2 (str): Naam van het tweede station
            distance (int): Afstand/tijd tussen de stations in minuten
        """
        self.station1 = station1
        self.station2 = station2
        self.distance = distance
        self.used = False

    def get_other_station(self, station: str) -> str:
        """
        Verkrijg de naam van het station aan de andere kant van de verbinding.
        
        Args:
            station (str): Naam van een station in de verbinding
            
        Retourneert:
            str: Naam van het andere station
        """
        if station == self.station1:
            return self.station2
        else:
            return self.station1

    def __str__(self) -> str:
        """
        String representatie van de Connection.
        
        Retourneert:
            str: Een string die de verbinding beschrijft
        """
        return f"Connection({self.station1} - {self.station2}, {self.distance} min)"
