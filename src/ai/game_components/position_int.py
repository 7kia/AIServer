from typing import List


class PositionInt:
    x: int = 0
    y: int = 0

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (
            self.x == other.x and
            self.y == other.y
        )

    def __mul__(self, other: int):
        return PositionInt(self.x * other, self.y * other)

    def __rmul__(self, other: int):
        return self.__mul__(other)

    def __add__(self, other: any):
        if type(other) is int:
            return PositionInt(self.x + other, self.y + other)
        elif type(other) is PositionInt:
            return PositionInt(self.x + other.x, self.y + other.y)
        raise NotImplementedError(f"PositionInt.__add__ for the {other} not implement")

    def __radd__(self, other):
        return self.__add__(other)

    def as_array(self) -> List[int]:
        return [self.x, self.y]


