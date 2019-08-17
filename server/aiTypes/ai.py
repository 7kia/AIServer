class Ai:
    id = None

    def __init__(self):
        pass

    @classmethod
    def get_commands(cls, game):
        return [{"commandName": "moveOrAttack", "arguments": {"arg1": "value1"}}]
