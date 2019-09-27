
Description
===========

##Library for getting a list of planes within a certain point radius
Usage example
from openskyapi.core import Point ,City
Target = Point (58.20,37.62)
Airplanes = Target.get_flights(267)
Citytarget = City("Tyumen")
Airplanescity = Citytarget._getflights()
