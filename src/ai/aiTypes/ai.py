class Ai:
    id = None
    location = None
    def __init__(self):
        pass

    def get_commands(self, game):
        return [{"commandName": "moveOrAttack", "arguments": {"arg1": "value1"}}]

    def generate_unit_positions(self, unit_counts):
        unit_positions = []
        for type_unit in unit_counts:
            for troop_size in unit_counts[type_unit]:
                amount = unit_counts[type_unit][troop_size]
                for i in range(amount):
                    unit_positions.append({
                        "type": type_unit,
                        "position": [0, 0],
                        "troopSize": troop_size,
                    })
        return unit_positions
