import unittest

import requests

from openskyapi.core import Point, City, API


class TestOpensky(unittest.TestCase):

    def test_city(self):
        with self.assertRaises(Exception):
            City('none')

    def test_create(self):
        self.assertTrue(Point(13, 33))
        self.assertTrue(City())

    def test_recive(self):
        # create coordinates and get check flight counts
        c = City('Berlin')
        airplanes = c.get_flights(290)
        self.assertIsNotNone(airplanes)
        self.assertFalse(airplanes.count(0))

    def test_invalid(self):
        # create coordinates and get negative flights
        with self.assertRaises(Exception):
            c = City('Berlin')
            c.get_flights(-77)

    def test_calculate_distance(self):
        # distance between these coordinates 2916
        distance = round(
            Point.calculate_distance(58.20, 68.25, 13.40, 52.52))
        self.assertEquals(distance, 2916)

    def test_url_opensky(self):
        r = requests.get(API + 'states/all')
        # if there is an answer everything is ok
        self.assertTrue(r.ok)
        # Check the contents
        self.assertTrue(len(r.json()) > 0)
        self.assertTrue('states' in r.json().keys())
