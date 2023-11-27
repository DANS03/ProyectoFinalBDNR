class Airport():
    airline:str
    flights:int
    def __init__(self, data) -> None:
        self.airline = data.airline
        self.flights = data.flights


