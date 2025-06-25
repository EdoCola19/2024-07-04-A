from dataclasses import dataclass

from model.sighting import Sighting


@dataclass
class Arco:
    Sighting1: Sighting
    Sighting2: Sighting

    def __str__(self):
        return f"Sight1 : {self.Sighting1} - Sight2: {self.Sighting2}"

    def __hash__(self):
        return hash(f"{self.Sighting1}-{self.Sighting2}")

