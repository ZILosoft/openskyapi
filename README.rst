
Description
===========

##Библиотека для получения списка из самолетов в радиусе определенной точки
Пример использования
from openskyapi.core import Point ,City
Target = Point (58.20,37.62)
Airplanes = Target._getflights()
Citytarget = City("Tyumen")
Airplanescity = Citytarget._getflights()
