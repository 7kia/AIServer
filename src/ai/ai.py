from .ai_command_generator import AiCommandGenerator, CommandName, Json
from src.ai.game_components.unit import Unit, UnitList
from src.ai.game_components.position import Position
from src.ai.game_components.game_state import GameState
from typing import List, Dict, Callable

from src.ai.game_components.game_data_extractor import UnitDict
from src.ai.game_components.location import Location, Bounds
from .ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from .game_components.position_generator import PositionGenerator
from .neural_network.technology_adapter.network_adapter import NetworkAdapter

CommandList = List[dict]


class Ai:
    id: int = None
    _location: Location = None
    _country: str = None
    _current_game_state: GameState = None
    _last_game_state: GameState = None
    _graph_density: List[List[int]] = None
    _is_train: bool = False
    _awards_definer_params: AwardsDefinerParams = None
    _time_to_tick: float = 0

    def get_commands(self, game: GameState) -> List[Json]:
        return []

    def generate_command_for_unit(self, unit: Unit, game: GameState) -> Json:
        return {}

    def generate_position(self, type_unit: str, troop_size: str, i: int, amount: int) -> Position:
        country_bound: Bounds = self._location.bounds_country[self._country]
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
                        "country": self._country,
                        "troopType": type_unit,
                        "position": [position.x, position.y],
                        "troopSize": troop_size,
                    })

        return AiCommandGenerator.generate_create_units_command(unit_positions)

    def get_location(self) -> Location:
        return self._location

    def set_location(self, location: Location):
        self._location = location

    def get_country(self) -> str:
        return self._country

    def set_country(self, country: str):
        self._country = country

    def set_current_game_state(self, game_state: GameState):
        if self._last_game_state is None:
            self._last_game_state = game_state
        self._current_game_state = game_state

    def get_current_game_state(self) -> GameState:
        return self._current_game_state

    def set_last_game_state(self, game_state: GameState):
        self._last_game_state = game_state

    def get_last_game_state(self) -> GameState:
        return self._last_game_state

    def set_graph_density(self, graph_density: List[List[int]]):
        self._graph_density = graph_density

    def set_train_mode(self, value: bool):
        self._is_train = value

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
        if not unit.state.stop:
            access_command_list.append(CommandName.stop_or_defence)

        if unit.state.attack:
            access_command_list.append(CommandName.retreat_or_storm)
        else:
            access_command_list.append(CommandName.move_or_attack)
        return access_command_list

    @staticmethod
    def _generate_target_position(unit_position: Position,
                                  changed_direction: Position, distance: float,
                                  map_bounds: Bounds) -> Position:
        result: Position = unit_position + (changed_direction * distance)
        if PositionGenerator.is_inside(map_bounds, unit_position):
            return result
        else:
            return PositionGenerator.move_to_map_border(unit_position, map_bounds)

    def is_train(self) -> bool:
        return self._is_train

    def set_awards_definer_params(self, awards_definer_params: AwardsDefinerParams):
        self._awards_definer_params = awards_definer_params

    def get_awards_definer_params(self) -> AwardsDefinerParams:
        return self._awards_definer_params

    def set_network_adapter(self, network_adapter: NetworkAdapter):
        # TODO 7kia настройку ИИ нужно было в AiDirector из AiManager вынести
        pass

    def set_troop_type(self, troop_type: str):
        raise IOError("troop_type can set only for neural networks")

    def update_timer(self):
        self._time_to_tick = self._current_game_state.current_time\
            .get_different_as_float(self._last_game_state.current_time.get_string_presentation())

    def time_end(self) -> bool:
        raise Exception("Ai not have timer")
