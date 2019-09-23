import unittest
from openskyapi.core import Point , City


class TestOpensky(unittest.TestCase):

    def test_city(self):
        with self.assertRaises(Exception): City('none')

    def test_create(self):
        self.assertTrue(Point(13,33))
        self.assertTrue(City())
    def test_recive(self):
        c=City('Berlin')
        Airplanes=c._getflights()
        self.assertTrue(Airplanes)
