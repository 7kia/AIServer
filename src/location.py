from typing import List, Dict
from src.ai.position import Position

Bounds = Dict[str, Position]
UnitAmounts = Dict[str, int]


class Location:
    id: str = "win_mechanic_test"
    name: str = "Win mechanic test"
    countries: List[str] = [
        "Novorossia",
        "Ukraine"
    ]
    bounds: Bounds = {
        "NE": Position(50.21621729063866, 40.330193359375016),
        "SW": Position(46.9890206199942, 35.3890859375)
    }
    bounds_country: Dict[str, Bounds] = {
        "Novorossia": {
            "NE": Position(
                48.12276619505541,
                39.802849609375016
            ),
            "SW": Position(
                47.869711326279216,
                37.74839990234375
            )
        },
        "Ukraine": {
            "NE": Position(
                49.767717668674585,
                37.028801757812516
            ),
            "SW": Position(
                47.10879329270628,
                35.32042138671875
            )
        }
    }
    resources: Dict[str, Dict[str, int]] = {
        "Novorossia": {
            "ammo": 100,
            "fuel": 0,
            "food": 0,
            "man": 0
        },
        "Ukraine": {
            "ammo": 300,
            "fuel": 0,
            "food": 0
        }
    }
    units: Dict[str, UnitAmounts] = {
        "Novorossia": {
            "tank": {
                "regiment": 1
            },
            "landbase": {
                "tactic": 1
            }
        },
        "Ukraine": {
            "landbase": {
                "tactic": 1
            }
        }
    }
    weapons: Dict[str, List[int]] = {  # TODO 7kia check correctness
        "Russia": [
            1984,
            1986
        ]
    }

    # def __init__(self):
    #     pass

    def __eq__(self, other):
        return vars(self) == vars(other)

