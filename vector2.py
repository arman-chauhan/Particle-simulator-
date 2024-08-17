import math


class Vector2:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x: float = x
        self.y: float = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector2(self.x / scalar, self.y / scalar)
        return NotImplemented

    def __str__(self):
        return f"x = {self.x} y = {self.y}"

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        len_ = self.length()
        if len_ == 0:
            return Vector2(0, 0)

        return Vector2(self.x / len_, self.y / len_)
