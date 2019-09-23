#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Библиотека для получения списка из самолетов в радиусе определенной точки
#

import requests
from math import radians, sin, cos, acos
from geographiclib.geodesic import Geodesic
from .city import cities


class Point:
    API = "https://opensky-network.org/api/states/all"

    def __init__(self, latitude, longitude):
        """
        Создает сущьность используя кординаты
        :param latitude:
        :param longitude:
        """
        self.LATITUDE = latitude
        self.LONGITUDE = longitude

    def _calculatedistance(self, lon1, lat1, lon2, lat2):
        """
        #вычесляем расстояние между двумя координатами, Warning! матан!
        за подробностями:
        https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
        :param lon1:
        :param lat1:
        :param lon2:
        :param lat2:
        :return: расстаяние float
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        return 6371 * (
            acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
        )

    def _getflights(self, square=270000):
        """
        Подключается к OpenSky Api запрашивает информацию о находящися самолетах в кадрате в square метрах между стенами
        после вычисляет расстаяние от self кардинат до самолета и возвращает список тех кто находится не дальше square метров

        :param square: Радиус в метрах (optional)
        :return: list
        """

        longitudemin = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 270, square)['lon2'], 2)  # запад
        latitudemin = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 180, square)['lat2'], 2)  # юг
        longitudemax = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 90, square)['lon2'], 2)  # восток
        latitudemax = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 0, square)['lat2'], 2)  # Север

        self.params = {'lamin': str(latitudemin),
                       'lomin': str(longitudemin),
                       'lamax': str(latitudemax),
                       'lomax': str(longitudemax)}

        try:
            self.resp = requests.get(self.API, params=self.params).json()
        except requests.exceptions.HTTPError as e:
            # если не получили 200 код
            print("Error: " + str(e))
        result = []
        # если ответ не пустой
        if not self.resp['states'] == None:
            for state in self.resp['states']:
                distance = (
                    self._calculatedistance(self.LONGITUDE, self.LATITUDE, state[5], state[6]))  # вычисляем дистанцию
                if distance < square:  # если меньше square тогда добавляем
                    result.append(
                        {'name': state[1],
                         'longitude': float(state[5]),
                         'latitude': float(state[6]),
                         'distance': round(distance, 1)})

        return result


class City(Point):

    def __init__(self, city='Berlin'):
        """
        создаеем сущность с коардинатами города из city.py
        :param city:
        """
        try:
            self.city = cities[city]
        except KeyError:
            raise Exception("'{}' нет такого города.".format(city))
        self.LATITUDE = self.city['latitude']
        self.LONGITUDE = self.city['longitude']
