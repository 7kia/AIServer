from .ai_commands import AiCommands, CommandName
from src.unit import Unit
from ..game import Game
from typing import List, Dict, Callable

from ..game_data_extractor import UnitDict, UnitList

CommandList = List[dict]


class Ai:
    id = None
    __location = None
    __country = None

    def __init__(self):
        pass

    def get_commands(self, game: Game):
        return [
            AiCommands.generate_move_or_attack_command(1, self.generate_position(None, None, None, None)),
            AiCommands.generate_retreat_or_storm_command(2, self.generate_position(None, None, None, None)),
            AiCommands.generate_stop_or_defence_command(3),
            # AiCommands.generate_take_train_command(4, 5),
            # AiCommands.generate_unload_train_command(4),
        ]

    def generate_position(self, type_unit, troop_size, i, amount):
        country_bound = self.__location["boundsCountry"][self.__country]
        return [
            (country_bound["NE"][0] + country_bound["SW"][0]) / 2,
            (country_bound["NE"][1] + country_bound["SW"][1]) / 2,
        ]

    def generate_unit_positions(self, unit_counts: Dict[str, str]):
        unit_positions: List[Dict[str, str]] = []
        for type_unit in unit_counts:
            for troop_size in unit_counts[type_unit]:
                amount = unit_counts[type_unit][troop_size]
                for i in range(amount):
                    unit_positions.append({
                        "country": self.__country,
                        "type": type_unit,
                        "position": self.generate_position(type_unit, troop_size, i, amount),
                        "troopSize": troop_size,
                    })

        return AiCommands.generate_create_units_command(unit_positions)

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_country(self):
        return self.__country

    def set_country(self, country):
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
