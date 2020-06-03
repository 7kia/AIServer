import unittest

from src.ai.ai_data_and_info.ai_data import AiData
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.ai_option_extractor import AiOptionExtractor
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.ai_manager import AiManager

ai_type: str = "neuron-network"
ai_address: str = "scout-layer"
ai_info = AiInfo(ai_type, ai_address)


class WhenUpdateAiThenAiManagerLog(unittest.TestCase):
    def setUp(self) -> None:
        self._ai_manager = AiManager()
        self.create_test_ai_and_logger(self._ai_manager)
        self._log_data()

    @classmethod
    def create_test_ai_and_logger(cls, ai_manager: AiManager):
        game_id: int = 0
        player_id: int = 1
        game_info = GameInfo(game_id, player_id, AiOptionExtractor.extract(
            {"troopType": "motorized"}
        ))
        ai_data = AiData(cls.generate_mock_location_info(), "Russia", {
            "graphDensity": [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ]
        })
        ai_manager.create_ai(
            ai_info=ai_info,
            game_info=game_info,
            ai_data=ai_data,
        )

    @classmethod
    def generate_mock_location_info(cls):
        return {
            "id": "win_mechanic_test",
            "name": "Win mechanic test",
            "countries": [
                "Russia",
                "NATO"
            ],
            "bounds": {
                "NE": [
                    50.21621729063866,
                    40.330193359375016
                ],
                "SW": [
                    46.9890206199942,
                    35.3890859375
                ]
            },
            "boundsCountry": {
                "Russia": {
                    "NE": [
                        48.12276619505541,
                        39.802849609375016
                    ],
                    "SW": [
                        47.869711326279216,
                        37.74839990234375
                    ]
                },
                "NATO": {
                    "NE": [
                        49.767717668674585,
                        37.028801757812516
                    ],
                    "SW": [
                        47.10879329270628,
                        35.32042138671875
                    ]
                }
            },
            "resources": {
                "Russia": {
                    "ammo": 100,
                    "fuel": 0,
                    "food": 0,
                    "man": 0
                },
                "NATO": {
                    "ammo": 300,
                    "fuel": 0,
                    "food": 0
                }
            },
            "units": {
                "Russia": {
                    "tank": {
                        "regiment": 1
                    },
                    "landbase": {
                        "tactic": 1
                    }
                },
                "NATO": {
                    "landbase": {
                        "tactic": 1
                    }
                }
            },
            "weapons": {
                "Russia": [
                    1984,
                    1986
                ]
            }
        }

    def test_current_game_state(self):
        self.assertEqual(True, False)

    def test_awards_for_current_game_state(self):
        self.assertEqual(True, False)

    def _log_data(self):
        pass


class WhenGameEndThenAiManagerLog(unittest.TestCase):
    def test_current_game_state(self):
        self.assertEqual(True, False)

    def test_summ_awards_for_current_game_state(self):
        self.assertEqual(True, False)

    def test_game_duration(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
