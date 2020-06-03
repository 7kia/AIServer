from src.ai.game_components.convert_self_to_json import Json, ConvertSelfToJson
from src.ai.game_components.game_units import GameUnits
from src.ai.game_components.person_unit_params import PersonUnitParams
from src.ai.game_components.sector_params import SectorParams


class GameState(ConvertSelfToJson):
    def __init__(self):
        # self.id: int = -1
        # self.users: Dict[str, str] = {}
        self.game_units: GameUnits = GameUnits()
        self.person_unit_params: PersonUnitParams = PersonUnitParams()
        self.sector_params: SectorParams = SectorParams()
        # Строка потому что время измеряется либо в тиках, либо секундах
        self.current_time: str = ""

    def as_json(self) -> Json:
        return {
            "game_units": self.game_units.as_json(),
            "person_unit_params": self.person_unit_params.as_json(),
            "sector_params": self.sector_params.as_json(),
            "current_time": self.current_time
        }
