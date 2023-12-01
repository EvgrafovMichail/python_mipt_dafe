import math
from typing import Generator, Any
from dataclasses import dataclass


@dataclass
class Vector3D:
    _x: float = 0
    _y: float = 0
    _z: float = 0

    def __iter__(self) -> Generator[float, None, None]:
        yield from (self._x, self._y, self._z)

    def __abs__(self) -> float:
        return sum(x_i ** 2 for x_i in self) ** 0.5

    def __bool__(self) -> bool:
        return abs(self) != 0

    def __eq__(self, other: Any) -> bool:
        self.__cheak_type__('==', other)

        return all(x_i == x_j for x_i, x_j in zip(self, other))

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        self.__cheak_type__('+', other)

        return Vector3D(
            *[x_i + x_j for x_i, x_j in zip(self, other)]
        )

    def __sub__(self, other):
        self.__cheak_type__('-', other)

        return self + -other

    def __mul__(self, scalar: float):
        scalar = float(scalar)

        return Vector3D(
            *[scalar * x_i for x_i in self]
        )

    def __rmul__(self, scalar: float):
        scalar = float(scalar)

        return self * scalar

    def __truediv__(self, scalar):
        scalar = float(scalar)

        return self * (1 / scalar)

    def __cheak_type__(self, operation: str, other: Any) -> None:
        if not isinstance(other, Vector3D):
            raise TypeError(
                f'objects of types Vector3D and {type(other).__name__}'
                'do not support operation {operation}'
            )

    def dot(self, other) -> float:
        self.__cheak_type__('dot', other)

        return sum(x_i * x_j for x_i, x_j in zip(self, other))

    def cross(self, other):
        self.__cheak_type__('cross', other)

        return Vector3D(
            self._y * other._z - self._z * other._y,
            self._z * other._x - self._x * other._z,
            self._x * other._y - self._y * other._x
        )

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z

def get_angle(self, other) -> float:
    self.__cheak_type__('get_angle', other)

    return math.acos((self.dot(other) / self.__abs__) / other.__abs__)

def dist_to_seg(a: Vector3D, b: Vector3D, c: Vector3D):
    ba = a - b
    if ba == Vector3D(0, 0, 0):
        return 0.0
    bc = c - b
    if bc == Vector3D(0, 0, 0):
        return (a - b).__abs__()
    cb = -bc
    ca = a - c
    if ca == Vector3D(0, 0, 0):
        return 0.0
    cos_abc = (ba.dot(bc)) / (abs(ba) * abs(bc))
    cos_acb = (cb.dot(ca)) / (abs(cb) * abs(ca))

    if cos_abc < 0 or cos_acb < 0:
        return min(abs(-ba), abs(-ca))
    else:
        if cos_abc > 1:
            cos_abc = 1
        return abs(ba) * (1 - cos_abc ** 2) ** 0.5  # ab sin abc = h

if __name__ == '__main__':
    a = Vector3D(2, 2, 2)
    b = Vector3D(0, 0, 0)
    c = Vector3D(1, 1, 1)
    print(dist_to_seg(a, b, c))