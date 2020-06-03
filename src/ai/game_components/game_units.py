from src.ai.game_components.convert_self_to_json import ConvertSelfToJson, Json
from src.ai.game_components.unit import UnitDict


class GameUnits(ConvertSelfToJson):
    own_units: UnitDict = {}
    visible_enemy_units: UnitDict = {}

    def __init__(self, own_units: UnitDict = {}, visible_enemy_units: UnitDict = {}):
        self.own_units = own_units
        self.visible_enemy_units = visible_enemy_units

    def as_json(self) -> Json:
        return {
            "own_units": self.own_units,
            "visible_enemy_units": self.visible_enemy_units
        }
