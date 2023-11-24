"""
- __init__() -  инициализация экземпляра класса. Конструирует новый объект типа Vector3D 
                из трех чисел с плавающей точкой(float). По умолчанию конструирует нулевой вектор. 
                Если пользователь попытается инициализировать объект нечисловыми типами, 
                необходимо бросить исключение;  
- __repr__() -  возвращает текстовую строку: `'Vector3D(x, y, z)'`, где x, y, z - значения компонент;  
- __abs__() -   возвращает длину вектора;  
- __bool__() -  возвращает True, если вектор ненулевой, иначе - False;  
- __eq__(other) - сравнивает два вектора, возвращает True, если векторы равны покомпонентно, иначе False;  
- __neg__() -   возвращает новый объект типа Vector3D, компоненты которого равны компонентам данного вектора, 
                домноженным на минус единицу;  
- __add__(other) - складывает два вектора, возвращает новый объект типа Vector3D - сумму;  
- __sub__(other) - вычитает вектор other из данного вектора, возвращает новый объект типа Vector3D - разность;  
- __mul__(scalar) - умножение вектора на скаляр слева, возвращает новый объект типа Vector3D - произведение;  
- __rmul__(scalar) - умножение вектора на скаляр справа, возвращает новый объект типа Vector3D - произведение;  
- __truediv__(scalar) - деление вектора на скаляр, возвращает новый объект типа Vector3D - частное;  
- dot(other) - возвращает результат скалярного произведения;  
- cross(other) - возвращает векторное произведение между векторами; 

"""
from typing import Generator, Any
from dataclasses import dataclass
import math

@dataclass
class Vector3D:
    _x: float = 0
    _y: float = 0
    _z: float = 0
    
    # def __init__(
    #     self,
    #     x: float = 0,
    #     y: float = 0,
    #     z: float = 0
    # ) -> None:
    #     self._x = x
    #     self._y = y
    #     self._z = z
        
    def __iter__(self) -> Generator[float, None, None]:
        yield from (self._x, self._y, self._z)
    
    # def __repr__(self) -> str:
    #     return f"Vector3D{self._x, self._y, self._z}"
    
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
            *[coord * scalar for coord in self]
        )
    
    def __rmul__(self, scalar: float):
        return self * scalar
    
    def __truediv__(self, scalar):
        scalar = float(scalar)
        return self * (1. / scalar)
    
    def dot(self, other) -> float:
        self._check_type("dot", other)

        return sum(x_i * x_j for x_i, x_j in zip(self, other))
    
    def cross(self, other):
        self._check_type("cross", other)

        return Vector3D(
            self._y * other._z - other._y * self._z,
            other._x * self._z - self._x * other._z,
            self._x * other._y - self._y * other._x
        )

    def _check_type(self, operation: str, other: Any) -> None:
        if not(isinstance(other, Vector3D)):
            raise TypeError(
                f"objects of types Vectro3D and {type(other).__name__} "
                f"do not support operation {operation}"
            )
    
    def get_angle(self, other) -> float:
        if not(isinstance(other, Vector3D)):
            raise TypeError(
                f"given objects' type is not Vector3D"
            )
        
        cos_of_angle = self * other / (abs(self) * abs(other))
        
        return math.acos(cos_of_angle)
        
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self._z


def get_angle(vector1: Vector3D, vector2: Vector3D, to_deg: bool) -> float:
        if not(isinstance(vector1, Vector3D) and isinstance(vector2, Vector3D)):
            raise TypeError(
                f"given objects' type is not Vector3D"
            )
        
        cos_of_angle = abs(vector1.dot(vector2)) / (abs(vector1) * abs(vector2))

        if to_deg:
            return math.acos(cos_of_angle) * 180 / math.pi
        else:
            return math.acos(cos_of_angle)


def dist_to_seg(vector_dot: Vector3D, vector_start: Vector3D, vector_end: Vector3D):
    if any(isinstance(vector_dot, Vector3D), isinstance(vector_start, Vector3D), isinstance(vector_end, Vector3D)):
            raise TypeError(
                f"given objects' type is not Vector3D"
            )
    
    line = vector_end - vector_start    #задающий вектор данной прямой
    line_beetwen_dots = vector_start - vector_dot   #vector_start здесь - это точка лежащая на прямой

    return abs(line_beetwen_dots.cross(line)) / abs(line)


if __name__ == "__main__":
    vectr1 = Vector3D(1, 0, 0)
    vectr2 = Vector3D(0, 1, 0)
    vectr3 = Vector3D(3,5,0)
    vectr4 = Vector3D(0,2,0)
    print(get_angle(vectr2, vectr1, True))
    print(get_angle(vectr2, vectr1, False))
    print(dist_to_seg(vectr1, vectr3, vectr4))