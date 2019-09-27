#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Library for getting a list of planes within a certain point radius
#

import requests
from geographiclib.geodesic import Geodesic
from math import radians, sin, cos, acos

from .city import cities

API = "https://opensky-network.org/api/"


class OpenskyApiException(Exception):
    pass


class Point:

    def __init__(self, latitude, longitude):
        """
        Create point with coordinates
        :param latitude:
        :param longitude:
        """
        self.LATITUDE = latitude
        self.LONGITUDE = longitude

    @staticmethod
    def calculate_distance(lon1, lat1, lon2, lat2):
        """
        calculate distance between the two coordinates
        for reference:
        https://medium.com/@petehouston/calculate-distance-of-two-locations-on-earth-using-python-1501b1944d97
        :param lon1:longitude of first point
        :param lat1:latitude of first point
        :param lon2:longitude of second point
        :param lat2:latitude of second point
        :return: float distance in km
        """
        earth_radius = 6371
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        return earth_radius * (
            acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
        )

    @staticmethod
    def _check_square_km(square):
        if square <= 0:
            raise OpenskyApiException("Invalid value {} km! Value must be positive".format(square))

    @staticmethod
    def _get_json(url, params=None):
        try:
            r = requests.get(API + url, params=params, timeout=30)
        except requests.exceptions.ConnectTimeout as e:
            raise OpenskyApiException("Timeout Соеденения: {}".format(e))
        if r.status_code == 200:
            return r.json()
        else:
            raise OpenskyApiException("Ошибка в запросе {0:d} - {1:s}".format(r.status_code, r.reason))

    def get_flights(self, square=270):
        """
        Connects to OpenSky Api requests information about aircraft in square between 'square' kilometers
        after calculating the distance from self coordinate to the plane and returns a list of those who are in round
        :param square: Radius in km (optional)
        :return: list
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
        if self.resp['states']:  # if the answer contains values in States
            for state in self.resp['states']:
                distance = (
                    self.calculate_distance(self.LONGITUDE,
                                            self.LATITUDE,
                                            state[5],
                                            state[6]))  # calculate the distance
                if distance < square:  # if less than square then add
                    result.append(
                        {'name': state[1],
                         'longitude': float(state[5]),
                         'latitude': float(state[6]),
                         'distance': round(distance, 1)})
        return result


class City(Point):

    def __init__(self, city='Berlin'):
        """
        create an entity with city coordinates from city.py
        :param city: string city name from City.py
        """
        try:
            self.city = cities[city]
        except KeyError:
            raise OpenskyApiException("'{}' no such city in city.py".format(city))
        self.LATITUDE = self.city['latitude']
        self.LONGITUDE = self.city['longitude']
        super(Point, self).__init__()
