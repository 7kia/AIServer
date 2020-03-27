from .ai_commands import AiCommands, CommandName, Json
from src.unit import Unit
from .position import Position
from ..game import Game
from typing import List, Dict, Callable

from ..game_data_extractor import UnitDict, UnitList
from ..location import Location, Bounds

CommandList = List[dict]

class Ai:
    id: int = None
    __location: Location = None
    __country: str = None

    def __init__(self):
        pass

    def get_commands(self, game: Game) -> List[Json]:
        return [
            AiCommands.generate_move_or_attack_command(1, self.generate_position(None, None, None, None)),
            AiCommands.generate_retreat_or_storm_command(2, self.generate_position(None, None, None, None)),
            AiCommands.generate_stop_or_defence_command(3),
            # AiCommands.generate_take_train_command(4, 5),
            # AiCommands.generate_unload_train_command(4),
        ]

    def generate_position(self, type_unit, troop_size, i, amount) -> Position:
        country_bound: Bounds = self.__location.bounds_country[self.__country]
        return Position(
            (country_bound["NE"].x + country_bound["SW"].x) / 2,
            (country_bound["NE"].y + country_bound["SW"].y) / 2
        )

    def generate_unit_positions(self, unit_counts: Dict[str, str]):
        unit_positions: List[Dict[str, str]] = []
        for type_unit in unit_counts:
            for troop_size in unit_counts[type_unit]:
                amount = unit_counts[type_unit][troop_size]
                for i in range(amount):
                    position: Position = self.generate_position(type_unit, troop_size, i, amount)
                    unit_positions.append({
                        "country": self.__country,
                        "type": type_unit,
                        "position": [position.x, position.y],
                        "troopSize": troop_size,
                    })

        return AiCommands.generate_create_units_command(unit_positions)

    def get_location(self) -> Location:
        return self.__location

    def set_location(self, location: Location):
        self.__location = location

    def get_country(self) -> str:
        return self.__country

    def set_country(self, country: str):
        self.__country = country

    @staticmethod
    def choose_units(
            choose_function: Callable[[Unit], bool],
            unit_dict: UnitDict) -> UnitList:
        unit_list: List[Unit] = []
        for unit_type in unit_dict.keys():
            for unit in unit_dict[unit_type]:
                if choose_function(unit):
                    unit_list.append(unit)
        return unit_list

    @staticmethod
    def generate_access_command_list(unit: Unit) -> List[str]:
        access_command_list: List[str] = []
        if unit.state.stop:
            if unit.state.attack:
                access_command_list.append(CommandName.retreat_or_storm)
            else:
                access_command_list.append(CommandName.move_or_attack)
        else:
            if unit.state.attack:
                access_command_list.append(CommandName.stop_or_defence)
                access_command_list.append(CommandName.retreat_or_storm)
            else:
                access_command_list.append(CommandName.stop_or_defence)
                access_command_list.append(CommandName.move_or_attack)
        return access_command_list
