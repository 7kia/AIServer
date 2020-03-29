from src.ai.ai import Ai
from src.ai.game_components.game import Game
from src.ai.game_components.game_data_extractor import UnitDict
from src.ai.game_components.game_units import GameUnits
from src.ai.game_components.location import Bounds
from src.ai.game_components.position import Position
from src.ai.game_components.unit import RegimentType, BaseType, SupportType, Unit
from src.ai.game_components.unit_state_extractor import UnitStatusFromJson, unit_states


class TestDataGenerator:
    @staticmethod
    def generate_test_unit_dictionary() -> GameUnits:
        return GameUnits(
            {
                "regiment": [Unit().set(0, RegimentType.tank.__str__())],
                "base": [Unit().set(1, BaseType.land_base.__str__())],
                "support": [Unit().set(2, SupportType.truck.__str__())],
            },
            {
                "regiments": [],
                "bases": [],
                "supports": [],
            },
        )

    @staticmethod
    def generate_unit_with_various_state(map_bounds: Bounds = None) -> GameUnits:
        positon: Position = Position()
        if map_bounds:
            positon = Position(
                (map_bounds["NE"].x + map_bounds["SW"].x) / 2,
                (map_bounds["NE"].y + map_bounds["SW"].y) / 2
            )
        return GameUnits(
            {
                "regiment": [
                    Unit().set(UnitStatusFromJson.UNIT_STATUS_STOP, RegimentType.tank.__str__(),
                               unit_states[UnitStatusFromJson.UNIT_STATUS_STOP],
                               positon),
                    Unit().set(UnitStatusFromJson.UNIT_STATUS_MARCH, RegimentType.tank.__str__(),
                               unit_states[UnitStatusFromJson.UNIT_STATUS_MARCH],
                               positon),
                    Unit().set(UnitStatusFromJson.UNIT_STATUS_ATTACK, RegimentType.tank.__str__(),
                               unit_states[UnitStatusFromJson.UNIT_STATUS_ATTACK],
                               positon),
                    Unit().set(UnitStatusFromJson.UNIT_STATUS_DEFENCE, RegimentType.tank.__str__(),
                               unit_states[UnitStatusFromJson.UNIT_STATUS_DEFENCE],
                               positon),
                    Unit().set(UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE, RegimentType.tank.__str__(),
                               unit_states[UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE],
                               positon),
                    Unit().set(UnitStatusFromJson.UNIT_STATUS_RETREAT, RegimentType.tank.__str__(),
                               unit_states[UnitStatusFromJson.UNIT_STATUS_RETREAT],
                               positon),
                ],
                "base": [Unit().set(11, BaseType.land_base.__str__())],
                "support": [Unit().set(12, SupportType.truck.__str__())],
            },
            {
                "regiments": [],
                "bases": [],
                "supports": [],
            },
        )



    @staticmethod
    def generate_test_game(game_id: int, player_id: int,
                           generate_unit_with_various_state: bool, map_bounds: Bounds = None) -> Game:
        game: Game = Game()
        game.id = game_id
        game.users = {player_id: {}}

        if generate_unit_with_various_state:
            game.game_units = TestDataGenerator.generate_unit_with_various_state(map_bounds)
        else:
            game.game_units = TestDataGenerator.generate_test_unit_dictionary()
        # "loserId": None,
        # "status": None,
        # "units": {},
        # "currentGameTime": None,
        # "battleMatrix": None,
        return game
