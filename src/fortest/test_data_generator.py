from src.game import Game
from src.game_data_extractor import UnitDict
from src.unit import RegimentType, BaseType, SupportType, Unit


class TestDataGenerator:
    @staticmethod
    def generate_test_unit_dictionary() -> UnitDict:
        return {
            "regiment": [Unit().set(0, RegimentType.tank.__str__())],
            "base": [Unit().set(1, BaseType.land_base.__str__())],
            "support": [Unit().set(2, SupportType.truck.__str__())],
        }

    @staticmethod
    def generate_test_game(game_id: int, player_id: int) -> Game:
        game: Game = Game()
        game.id = game_id
        game.users = {player_id: {}}
        game.unit_dictionary = TestDataGenerator.generate_test_unit_dictionary()
        # "loserId": None,
        # "status": None,
        # "units": {},
        # "currentGameTime": None,
        # "battleMatrix": None,
        return game
