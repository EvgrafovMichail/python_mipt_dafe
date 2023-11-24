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


class Vector3D:
    _x: float
    _y: float
    _z: float
    
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z: float =0
    ) -> None:
        pass
        
    def __iter__(self) -> Generator[float, None, None]:
        pass
    
    def __repr__(self) -> str:
        pass
    
    def __abs__(self) -> float:
        pass
    
    def __bool__(self) -> bool:
        pass
    
    def __eq__(self, other: Any) -> bool:    
        pass
    
    def __neg__(self):
        pass
    
    def __add__(self, other):
        pass
    
    def __sub__(self, other):
        pass
    
    def __mul__(self, scalar: float):
        pass
    
    def __rmul__(self, scalar: float):
        pass
    
    def __truediv__(self, scalar):
        pass
    
    def dot(self, other) -> float:
        pass
    
    def cross(self, other):
        pass
        
    @property
    def x(self) -> float:
        pass
    
    @property
    def y(self) -> float:
        pass
    
    @property
    def z(self) -> float:
        pass