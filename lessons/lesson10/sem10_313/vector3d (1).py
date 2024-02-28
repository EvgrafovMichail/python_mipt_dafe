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
from math import acos


@dataclass
class Vector3D:
    _x: float = 0
    _y: float = 0 
    _z: float = 0
        
    def __iter__(self) -> Generator[float, None, None]:
        yield from (self._x, self._y,self._z)
        
    
    def __abs__(self) -> float:
        return sum(x_i ** 2 for x_i in self)**0.5
    def __bool__(self) -> bool:
        return abs(self) != 0
    
    def __eq__(self, other: Any) -> bool: 
        self._check_type('==',other)   
        
        return all(x_i == x_j for x_i, x_j in zip(self, other))
    
    def __neg__(self):
        return Vector3D(self._x * -1,self._y* -1, self._z *-1)
    
    def __add__(self, other):
        self._check_type('+',other)
        return Vector3D(*[x_i + x_j for x_i, x_j in zip(self, other)])
    
    def __sub__(self, other):
        self._check_type('-', other)
        return self + -other
    
    def __mul__(self, scalar: float):
        scalar = float(scalar)
        return Vector3D(*[x_i * scalar for x_i in zip(self)])

        
    
    def __rmul__(self, scalar: float):
        scalar = float(scalar)
        return self * scalar
    
    def __truediv__(self, scalar):
        scalar = float(scalar)
        return self * (1. / scalar)
    
    def dot(self, other) -> float:
        self._check_type('dot', other)
        return sum(x_i*x_j for x_i,x_j in zip(self, other))
    
    def cross(self, other):
        self._check_type('cross', other)
        return Vector3D(
            self.y * other.z - other.y * self.z,
            self.x * other.z - other.x * self.z,
            self.x * other.y - other.x * self.y,
        )
    
    def get_angle(self, other):
        self._check_type('get_angle', other)
        return acos(self.dot(other)/abs(self)/abs(other))
    def get_seq(self, other):
        self._check_type('get_angle', other)
        return sum((x_i-x_j)**2 for x_i,x_j in zip(self,other))**0.5
        
        

    def _check_type(self, operation: str, other: Any):
        if not isinstance(other, Vector3D):
            raise TypeError(
                f'objects of types Vector3D and {type(other).__name__}'
                f'do not support operation {operation}'
            )
        
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self.z
    
print(Vector3D(1, 1, 1).x)
triss = Vector3D(3,2,1)
kolbasa = Vector3D(1, 1, 1)
print(abs(kolbasa))
print(kolbasa.get_seq(triss))

# if __name__ == '__main__':
#     vector = Vector3D(1,2,3)
#     print(f"vector:{vector}")
#     print(iter(vector))
#     print(abs(vector))
#     # assert vector
#     vec_2 = Vector3D(3,2,1)
#     # assert vec_2 == vector
#     print(vector.__neg__())