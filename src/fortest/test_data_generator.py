from src.game import Game
from src.game_data_extractor import UnitDict
from src.unit import RegimentType, BaseType, SupportType, Unit
from src.unit_state_extractor import UnitStatusFromJson, unit_states


class TestDataGenerator:
    @staticmethod
    def generate_test_unit_dictionary() -> UnitDict:
        return {
            "regiment": [Unit().set(0, RegimentType.tank.__str__())],
            "base": [Unit().set(1, BaseType.land_base.__str__())],
            "support": [Unit().set(2, SupportType.truck.__str__())],
        }

    @staticmethod
    def generate_unit_with_various_state() -> UnitDict:
        return {
            "regiment": [
                Unit().set(UnitStatusFromJson.UNIT_STATUS_STOP, RegimentType.tank.__str__(),
                           unit_states[UnitStatusFromJson.UNIT_STATUS_STOP]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_MARCH, RegimentType.tank.__str__(),
                           unit_states[UnitStatusFromJson.UNIT_STATUS_MARCH]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_ATTACK, RegimentType.tank.__str__(),
                           unit_states[UnitStatusFromJson.UNIT_STATUS_ATTACK]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_DEFENCE, RegimentType.tank.__str__(),
                           unit_states[UnitStatusFromJson.UNIT_STATUS_DEFENCE]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE, RegimentType.tank.__str__(),
                           unit_states[UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_RETREAT, RegimentType.tank.__str__(),
                           unit_states[UnitStatusFromJson.UNIT_STATUS_RETREAT]),
            ],
            "base": [Unit().set(11, BaseType.land_base.__str__())],
            "support": [Unit().set(12, SupportType.truck.__str__())],
        }

    @staticmethod
    def generate_test_game(game_id: int, player_id: int, generate_unit_with_various_state: bool) -> Game:
        game: Game = Game()
        game.id = game_id
        game.users = {player_id: {}}

        if generate_unit_with_various_state:
            game.unit_dictionary = TestDataGenerator.generate_unit_with_various_state()
        else:
            game.unit_dictionary = TestDataGenerator.generate_test_unit_dictionary()
        # "loserId": None,
        # "status": None,
        # "units": {},
        # "currentGameTime": None,
        # "battleMatrix": None,
        return game
