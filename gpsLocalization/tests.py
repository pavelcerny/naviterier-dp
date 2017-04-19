from django.test import TestCase

from gpsLocalization import data
from mathfunctions.functions import getAngleOfTwoSegments
from gpsLocalization.functions import _clusterPath, _getEdge, _uniteLastWithFirst, getEdgesInCluster


class SimpleTest(TestCase):

    def test_getsegment_closed_path(self):
        sidewalk = [1,3, 7, 6, 1]
        self.assertEqual(_getEdge(1, sidewalk), (3, 7))
        self.assertEqual(_getEdge(4, sidewalk), (1, 3))

    def test_getsegment_open_path(self):
        sidewalk = [1, 3, 7, 6 , 5]
        self.assertEqual(_getEdge(1, sidewalk), (3, 7))
        self.assertEqual(_getEdge(4, sidewalk), None)
        self.assertEqual(_getEdge(5, sidewalk), None)

    def test_angle_two_segments_90_degrees(self):
        a = {
            'Latitude': 0,
            'Longitude': 1
        }
        b = {
            'Latitude': 0,
            'Longitude': 0
        }
        c = {
            'Latitude': 1,
            'Longitude': 0
        }

        s = (a,b)
        t = (b,c)
        self.assertEqual(getAngleOfTwoSegments(s,t), 90)
        self.assertEqual(getAngleOfTwoSegments(t,s), 90)

    def test_angle_two_segments_180_degrees(self):
        a = {
            'Latitude': 0,
            'Longitude': 1
        }
        b = {
            'Latitude': 0,
            'Longitude': 0
        }
        c = {
            'Latitude': 0,
            'Longitude': -1
        }

        s = (a,b)
        t = (b,c)
        self.assertEqual(getAngleOfTwoSegments(s,t), 180)
        self.assertEqual(getAngleOfTwoSegments(t,s), 180)

    def test_angle_two_segments_135_degrees(self):
        a = {
            'Latitude': 0,
            'Longitude': 1
        }
        b = {
            'Latitude': 0,
            'Longitude': 0
        }
        c = {
            'Latitude': 1,
            'Longitude': -1
        }

        s = (a,b)
        t = (b,c)
        self.assertEqual(getAngleOfTwoSegments(s,t), 135)
        self.assertEqual(getAngleOfTwoSegments(t,s), 135)

    def test_cluster_closed_path(self):
        sidewalk = [{
            'Latitude': 0,
            'Longitude': -1
        },{
            'Latitude': 0,
            'Longitude': -2
        },{
            'Latitude': 1,
            'Longitude': -2
        },{
            'Latitude': 1.5,
            'Longitude': -1.8
        },{
            'Latitude': 1,
            'Longitude': 0
        },{
            'Latitude': 0,
            'Longitude': 0
        },{
            'Latitude': 0,
            'Longitude': -1
        }]

        labels = [1,2,2,3,4,1]

        self.assertEqual(_clusterPath(sidewalk), labels)

    def test_cluster_open_path(self):
        sidewalk = [{
            'Latitude': 0,
            'Longitude': -1
        },{
            'Latitude': 0,
            'Longitude': -2
        },{
            'Latitude': 1,
            'Longitude': -2
        },{
            'Latitude': 1.5,
            'Longitude': -1.8
        },{
            'Latitude': 1,
            'Longitude': 0
        },{
            'Latitude': 0,
            'Longitude': 0
        },{
            'Latitude': 1,
            'Longitude': -1
        }]

        labels = [1,2,2,3,4,5]

        self.assertEqual(_clusterPath(sidewalk), labels)

    def test_unite_last_with_first(self):
        labels = [1,1,2,3,4,4,5,5,5]
        united = [1,1,2,3,4,4,1,1,1]
        self.assertEqual(_uniteLastWithFirst(labels[1], labels[-1], labels), united)

class FunctionsTest(TestCase):
    def test_get_edges_in_cluster(self):

        clusterId_v1 = 1
        clusterId_v2 = 2
        clusters = [1,2,2,3,1]
        path = [1,2,3,4,5,6]

        self.assertEqual(getEdgesInCluster(clusterId_v1, clusters, path), [(1,2),(5,6)])
        self.assertEqual(getEdgesInCluster(clusterId_v2, clusters, path), [(2,3),(3,4)])

class DataTest(TestCase):
    def test_get_segments(self):
        lat = 50.0792784
        lon = 14.4204132
        radius = 70

        segments = data.getSegments(lat, lon, radius)

        self.assertIsNotNone(segments)

