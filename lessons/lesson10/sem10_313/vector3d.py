from typing import Generator, Any
from dataclasses import dataclass
import math

@dataclass
class Vector3D:
    _x: float = 0
    _y: float = 0
    _z: float = 0


    def __iter__(self) -> Generator[float, None, None]:
        yield from (self.x, self.y, self.z)

    def __abs__(self) -> float:
        return sum(x_i ** 2 for x_i in self) ** 0.5

    def __bool__(self) -> bool:
        return abs(self) != 0

    def __eq__(self, other: Any) -> bool:
        self._check_type('==', other)
        return all(x_i == x_j for x_i, x_j in zip(self, other))

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        self._check_type('+', other)
        return Vector3D(
            *[x_i + x_j for x_i, x_j in zip(self, other)]
        )

    def __sub__(self, other):
        self._check_type('-', other)
        return self + -other

    def __mul__(self, scalar: float):
        scalar = float(scalar)
        return Vector3D(
            *[x_i * scalar for x_i in self]
        )

    def __rmul__(self, scalar: float):
        return self * scalar

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def __truediv__(self, scalar):
        scalar = float(scalar)
        return self * (1 / scalar)

    def dot(self, other) -> float:
        self._check_type('dot', other)
        return sum(x_i * x_j for x_i, x_j in zip(self, other))

    def cross(self, other):
        self._check_type('cross', other)
        return Vector3D(
            self._y * other._z - other._y * self._z,
            self._z * other._x - other._z * self._x,
            self._x * other._y - other._x * self._y
        )

    def _check_type(self, operation: str, other: Any):
        if not isinstance(other, Vector3D):
            raise TypeError(
                f'objects of type Vector3D and {type(other).__name__} 
                do not support operation {operation}'
            )

    def get_angle(self, other, to_deg=False) -> float:
        if to_deg:
            return math.degrees(math.acos(self.dot(other) / (abs(self) * abs(other))))
        return math.acos(self.dot(other) / (abs(self) * abs(other)))

    @property
    def x(self) -> float:
        return self.x

    @property
    def y(self) -> float:
        return self.y

    @property
    def z(self) -> float:
        return self.z

def dist_to_seg(self: Vector3D, other: Vector3D, dot: Vector3D):
    if dot(other - self, self - dot) <= 0:
        return self.dist(dot)
    elif dot(other - self, other - dot) <= 0:
        return other.dist(dot)
    else:
        return abs((dot - self).cross(other - self)) / abs(other - self)