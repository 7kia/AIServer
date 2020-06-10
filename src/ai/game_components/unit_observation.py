from src.ai.game_components.position import Position
from src.ai.game_components.position_int import PositionInt
from src.ai.game_components.sector_params import SectorParams
from src.ai.game_components.unit import Unit


class UnitObservation:
    def __init__(self):
        self.own_organization: float = 0
        self.own_composition: float = 0
        self.sector: PositionInt = PositionInt()

        self.own_sum_info: float = 0
        self.own_max_info: float = 0
        self.enemy_sum_info: float = 0
        self.enemy_max_info: float = 0

    def set(self, sector_params: SectorParams, unit: Unit):
        self.own_organization = unit.organization
        self.own_composition = unit.composition

        self.sector = sector_params.find_unit_index(unit)
        self.own_sum_info = sector_params.own_sum_info[self.sector.y][self.sector.x]
        self.own_max_info = sector_params.own_max_info[self.sector.y][self.sector.x]
        self.enemy_sum_info = sector_params.enemy_sum_info[self.sector.y][self.sector.x]
        self.enemy_max_info = sector_params.enemy_max_info[self.sector.y][self.sector.x]

