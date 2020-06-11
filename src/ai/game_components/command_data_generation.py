from src.ai.game_components.position import Position


class CommandDataGeneration:
    def __init__(self, unit_id: int, position: Position):
        self.id: int = unit_id
        self.position: Position = position
