class Ai:
    id = None
    __location = None
    __country = None

    def __init__(self):
        pass

    @classmethod
    def generate_move_or_attack_command(cls, unit_id, position):
        return {
            "commandName": "move_or_attack",
            "arguments": {
                "unit_id": unit_id,
                "position": position
            }
        }

    @classmethod
    def generate_retreat_or_storm_command(cls, unit_id, position):
        return {
            "commandName": "retreat_or_storm",
            "arguments": {
                "unit_id": unit_id,
                "position": position
            }
        }

    @classmethod
    def generate_take_train_command(cls, unit_id, passenger_id):
        return {
            "commandName": "take_train",
            "arguments": {
                "unit_id": unit_id,
                "passenger_id": passenger_id
            }
        }

    @classmethod
    def generate_unload_train_command(cls, unit_id):
        return {
            "commandName": "unload_train",
            "arguments": {
                "unit_id": unit_id
            }
        }

    @classmethod
    def generate_stop_or_defence_command(cls, unit_id):
        return {
            "commandName": "stop_or_defence",
            "arguments": {
                "unit_id": unit_id
            }
        }

    def get_commands(self, game):
        return [
            Ai.generate_move_or_attack_command(1, self.generate_position(None, None, None, None)),
            Ai.generate_retreat_or_storm_command(2, self.generate_position(None, None, None, None)),
            Ai.generate_stop_or_defence_command(3),
            Ai.generate_take_train_command(4, 5),
            Ai.generate_unload_train_command(4),
        ]

    def generate_position(self, type_unit, troop_size, i, amount):
        country_bound = self.__location["boundsCountry"][self.__country]
        return [
            (country_bound["NE"][0] + country_bound["SW"][0]) / 2,
            (country_bound["NE"][1] + country_bound["SW"][1]) / 2,
        ]

    def generate_unit_positions(self, unit_counts):
        unit_positions = []
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
        return unit_positions

    def get_location(self):
        return self.__location

    def set_location(self, location):
        self.__location = location

    def get_country(self):
        return self.__country

    def set_country(self, country):
        self.__country = country
