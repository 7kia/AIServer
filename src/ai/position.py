class Position:
    x: float = 0
    y: float = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
            self.x == other.x and
            self.y == other.y
        )
