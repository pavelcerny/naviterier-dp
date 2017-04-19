from django.test import TestCase

from mathfunctions.functions import minWithIdx, dist2, minus, dot, length_squared, project

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):

    def test_min_value(self):
        """ test minWithIdx returns minimum on index 2 for given array"""
        a = [3,3,-2,7, 5]
        val, idx = minWithIdx(a)
        self.assertEqual(val,a[2])

    def test_idx_value(self):
        """ test minWithIdx returns index 3 for given array """
        a = [3, 3, -2, 7, 5]
        val, idx = minWithIdx(a)
        self.assertEqual(idx,2)

    def test_left(self):
        """ test dist2 of point one unit from one of the endpoint is 1^2 """
        d = dist2(0, 0, 1, 0, -1, 0)
        self.assertEqual(d,pow(1,2))

    def test_between(self):
        """ test dist2 of point lying on the segment line is 0 """
        d = dist2(0, 0, 1, 0, 0.5, 0)
        self.assertEqual(d,0)

    def test_between_in_distance(self):
        """ test dist2 of point lying on a line parallel to the segment line the distance of these two lines"""
        d = dist2(0, 0, 1, 0, 0.5, 1)
        self.assertEqual(d, pow(1,2))

    def test_minus(self):
        dif = minus((3,4),(7,6))
        self.assertEqual(dif,(3-7,4-6))

    def test_dot(self):
        d = dot((3,4), (7,6))
        self.assertEqual(d,3*7+4*6)

    def test_squared_distance(self):
        l2 = length_squared((3,4),(7,6))
        self.assertEqual(l2, ( (3-7)*(3-7) ) + ( (4-6)*(4-6) ) )

    def test_projection_point_on_line(self):
        a=(0,0)
        b=(1,0)
        p=(0.5,0)
        projection = project(a,b,p)
        expected=(0.5,0)
        self.assertEqual(projection,expected)

    def test_projection_point_on_left_from_line(self):
        a = (0, 0)
        b = (1, 0)
        p = (-1, 0)
        projection = project(a, b, p)
        expected = a
        self.assertEqual(projection, expected)

    def test_projection_point_on_right_from_line(self):
        a = (0, 0)
        b = (1, 0)
        p = (3, 1)
        projection = project(a, b, p)
        expected = b
        self.assertEqual(projection, expected)

    def test_projection_point_next_to_line(self):
        a = (0, 0)
        b = (1, 0)
        p = (0.5, 1)
        projection = project(a, b, p)
        expected = (0.5, 0)
        self.assertEqual(projection, expected)
