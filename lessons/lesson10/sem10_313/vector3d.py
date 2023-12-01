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
            *[scalar * x_i  for x_i in self]
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
    
    def get_angle(self, other) -> float:
        self.__cheak_type__('get_angle', other)

        return math.acos((self.dot(other) / self.__abs__) / other.__abs__)
    
    def dist_to_seg(p1, p2, p3, p4 ):
        v1 = Vector3D(p2 - p1)
        v2 = Vector3D(p4 - p3)

        return v1.dot(v1.cross(v2)) / v1.cross(v2).__abs__

        
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self._z
    

if __name__ == '__main__':
    a = Vector3D(1, 1, 1)
    a2 = Vector3D(2, 1, 1)
    b = Vector3D(0, 0, 0)
    b2 = Vector3D(1, 0, 0)
    print(a.dist_to_seg(a2, b, b2))