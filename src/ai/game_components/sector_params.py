from typing import List

from src.ai.game_components.convert_self_to_json import ConvertSelfToJson, Json
from src.ai.game_components.position_int import PositionInt
from src.ai.game_components.unit import Unit


class SectorParams(ConvertSelfToJson):
    def __init__(self):
        self.ownUnitToSectors: List[List[List[Unit]]] = []
        self.enemyUnitToSectors: List[List[List[Unit]]] = []

        self.own_sum_info: List[List[float]] = []
        self.own_max_info: List[List[float]] = []
        self.enemy_sum_info: List[List[float]] = []
        self.enemy_max_info: List[List[float]] = []

    def find_unit_index(self, unit: Unit) -> PositionInt:
        for row_index in range(len(self.ownUnitToSectors)):
            row: List[List[Unit]] = self.ownUnitToSectors[row_index]
            for cell_index in range(len(row)):
                cell: List[Unit] = row[cell_index]
                for unit_from_cell in cell:
                    if unit_from_cell.id == unit.id:
                        return PositionInt(cell_index, row_index)

    def as_json(self) -> Json:
        return {
            "ownUnitToSectors": self.ownUnitToSectors,
            "enemyUnitToSectors": self.enemyUnitToSectors,

            "ownSumInfo": self.own_sum_info,
            "ownMaxInfo": self.own_max_info,
            "enemySumInfo": self.enemy_sum_info,
            "enemyMaxInfo": self.enemy_max_info,
        }
