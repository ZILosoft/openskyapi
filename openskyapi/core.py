#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Библиотека для получения списка из самолетов в радиусе определенной точки
#

import logging
from math import radians, sin, cos, acos

import requests
from geographiclib.geodesic import Geodesic

from .city import cities

logger = logging.getLogger('opensky_api')
logger.addHandler(logging.NullHandler())


class Point:
    API = "https://opensky-network.org/api/"

    def __init__(self, latitude, longitude):
        """
        Создает сущьность используя кординаты
        :param latitude:
        :param longitude:
        """
        self.LATITUDE = latitude
        self.LONGITUDE = longitude

    @staticmethod
    def _calculate_distance(lon1, lat1, lon2, lat2):
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
        earth_radius = 6371
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        return earth_radius * (
            acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
        )

    @staticmethod
    def _check_square_km(square):
        if square <= 0:
            raise ValueError("Неверное значение км {:f}! должно быть положительным ".format(square))

    def _get_json(self, url, params=None):
        try:
            r = requests.get(self.API + url, params=params, timeout=0.001)
        except requests.exceptions.ConnectTimeout as e:
            logger.error("Timeout Соеденения: {}".format(e))
            return None
        if r.status_code == 200:
            return r.json()
        else:
            logger.debug("Ошибка в запросе {0:d} - {1:s}".format(r.status_code, r.reason))
        return None

    def get_flights(self, square=270):
        """
        Подключается к OpenSky Api запрашивает информацию о находящися самолетах в кадрате в square километрах между стенами
        после вычисляет расстаяние от self кардинат до самолета и возвращает список тех кто находится не дальше square метров

        :param square: Радиус в километрах (optional)
        :return:  Лист, в случаи каких то проблем None
        """

        square = round(square, 0)
        self._check_square_km(square)
        square *= 1000
        longitude_min = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 270, square)['lon2'], 2)  # запад
        latitude_min = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 180, square)['lat2'], 2)  # юг
        longitude_max = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 90, square)['lon2'], 2)  # восток
        latitude_max = round(Geodesic.WGS84.Direct(self.LATITUDE, self.LONGITUDE, 0, square)['lat2'], 2)  # Север

        self.params = {'lamin': str(latitude_min),
                       'lomin': str(longitude_min),
                       'lamax': str(latitude_max),
                       'lomax': str(longitude_max)}

        self.resp = self._get_json('states/all', self.params)

        result = []
        if self.resp:  # если ответ пустой возвращеаем None
            if self.resp['states']:  # если ответ содержит значения в States
                for state in self.resp['states']:
                    distance = (
                        self._calculate_distance(self.LONGITUDE, self.LATITUDE, state[5],
                                                 state[6]))  # вычисляем дистанцию
                    if distance < square:  # если меньше square тогда добавляем
                        result.append(
                            {'name': state[1],
                             'longitude': float(state[5]),
                             'latitude': float(state[6]),
                             'distance': round(distance, 1)})
        else:
            return None

        return result


class City(Point):

    def __init__(self, city='Berlin'):
        """
        создаеем сущность с коардинатами города из city.py
        :param city: string Имя города из City.py
        """
        try:
            self.city = cities[city]
        except KeyError:
            raise Exception("'{}' нет такого города.".format(city))
        self.LATITUDE = self.city['latitude']
        self.LONGITUDE = self.city['longitude']
