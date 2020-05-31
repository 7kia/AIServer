from src.ai.game_components.unit import UnitDict


class GameUnits:
    own_units: UnitDict = {}
    visible_enemy_units: UnitDict = {}

    def __init__(self, own_units: UnitDict = {}, visible_enemy_units: UnitDict = {}):
        self.own_units = own_units
        self.visible_enemy_units = visible_enemy_units
