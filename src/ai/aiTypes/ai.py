class Ai:
    id = None
    location = None
    def __init__(self):
        pass

    def get_commands(self, game):
        return [{"commandName": "moveOrAttack", "arguments": {"arg1": "value1"}}]
