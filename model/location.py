from dataclasses import dataclass


@dataclass
class Location:
    Location: str
    latitude: float
    longitude: float

    def __hash__(self):
        # vorrei avere una hash function perché queste location potrebbero essere implementate in una lista
        return hash(self.Location)  # tanto le location sono univoche

    def __str__(self):
        return self.Location
