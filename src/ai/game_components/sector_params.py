from typing import List

from src.ai.game_components.convert_self_to_json import ConvertSelfToJson, Json
from src.ai.game_components.unit import Unit


class SectorParams(ConvertSelfToJson):
    def __init__(self):
        self.ownUnitToSectors: List[List[Unit]] = []
        self.enemyUnitToSectors: List[List[Unit]] = []

        self.ownSumInfo: List[List[float]] = []
        self.ownMaxInfo: List[List[float]] = []
        self.enemySumInfo: List[List[float]] = []
        self.enemyMaxInfo: List[List[float]] = []

    def as_json(self) -> Json:
        return {
            "ownUnitToSectors": self.ownUnitToSectors,
            "enemyUnitToSectors": self.enemyUnitToSectors,

            "ownSumInfo": self.ownSumInfo,
            "ownMaxInfo": self.ownMaxInfo,
            "enemySumInfo": self.enemySumInfo,
            "enemyMaxInfo": self.enemyMaxInfo,
        }
