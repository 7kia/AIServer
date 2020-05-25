from typing import List

from src.ai.game_components.unit import Unit


class SectorParams:
    def __init__(self):
        self.ownUnitToSectors: List[List[Unit]] = []
        self.enemyUnitToSectors: List[List[Unit]] = []

        self.ownSumInfo: List[List[float]] = []
        self.ownMaxInfo: List[List[float]] = []
        self.enemySumInfo: List[List[float]] = []
        self.enemyMaxInfo: List[List[float]] = []
