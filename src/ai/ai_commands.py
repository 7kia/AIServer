from typing import List, Dict
from enum import Enum
Json = Dict[str, any]


class CommandName(Enum):
    create_units: str = "create_units"
    move_or_attack: str = "move_or_attack"
    retreat_or_storm: str = "retreat_or_storm"
    take_train: str = "take_train"
    unload_train: str = "unload_train"
    stop_or_defence: str = "stop_or_defence"


class AiCommands:
    @classmethod
    def generate_create_unit_data(cls,
                                  country: str, troop_type: str,
                                  position: List[float], troop_size: str) -> Json:
        return {
            "country": country,
            "type": troop_type,
            "position": position,
            "troopSize": troop_size,
        }

    @classmethod
    def generate_create_units_command(cls, units_data: List[Dict[str, str]]) -> Json:
        return {
            "commandName": "create_units",
            "arguments": {
                "unit_data": units_data
            }
        }

    @classmethod
    def generate_move_or_attack_command(cls, unit_id: int, position: List[float]) -> Json:
        return {
            "commandName": "move_or_attack",
            "arguments": {
                "unit_id": unit_id,
                "position": position
            }
        }

    @classmethod
    def generate_retreat_or_storm_command(cls, unit_id: int, position: List[float]) -> Json:
        return {
            "commandName": "retreat_or_storm",
            "arguments": {
                "unit_id": unit_id,
                "position": position
            }
        }

    @classmethod
    def generate_take_train_command(cls, unit_id: int, passenger_id: int) -> Json:
        return {
            "commandName": "take_train",
            "arguments": {
                "unit_id": unit_id,
                "passenger_id": passenger_id
            }
        }

    @classmethod
    def generate_unload_train_command(cls, unit_id: int) -> Json:
        return {
            "commandName": "unload_train",
            "arguments": {
                "unit_id": unit_id
            }
        }

    @classmethod
    def generate_stop_or_defence_command(cls, unit_id: int) -> Json:
        return {
            "commandName": "stop_or_defence",
            "arguments": {
                "unit_id": unit_id
            }
        }
