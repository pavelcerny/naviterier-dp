class UserPath:
    def __init__(self, beforeCorner, afterCorner):
        self.beforeCorner = beforeCorner
        self.afterCorner = afterCorner

    def getCorner(self):
        # corner is on last coordinates beforeCorner
        return self.beforeCorner[-1]

    def getRadius(self):
        return 70

    def getLastPosition(self):
        return self.afterCorner[-1]

    def getBeforeCorner(self):
        return self.beforeCorner

    def getAfterCorner(self):
        return self.afterCorner


class Sidewalks:
    pass

class Segment:
    def __init__(self,a,b):
        self.a = a
        self.b = b

class Section:
    pass


def tuple2latlon(t):
    lat = t[0]
    lon = t[1]

    return {
        'lat':lat,
        'lon':lon
    }


def tuple2latitudelongitude(t):
    lat = t[0]
    lon = t[1]

    return {
        'Latitude': lat,
        'Longitude': lon
    }


def latitudelongitude2tuple(ll):
    return ll['Latitude'] , ll['Longitude']


def latlon2tuple(ll):
    return ll['lat'] , ll['lon']


def tuple2Latlon_array(tuples):
    latlons = []
    for t in tuples:
        latlons.append(tuple2latlon(t))
    return latlons


def tuple2LatitudeLongitude_array(tuples):
    latlons = []
    for t in tuples:
        latlons.append(tuple2latitudelongitude(t))
    return latlons


def Latitudelongitude2Tuple_array(latlon):
    tuples = []
    for ll in latlon:
        tuples.append(latitudelongitude2tuple(ll))
    return tuples


def latlon2tuple_array(latlon):
    tuples = []
    for ll in latlon:
        tuples.append(latlon2tuple(ll))
    return tuples


def naviterierSegments2points(segments):
    n = len(segments)
    points = [[]]*n
    for i in range(n):
        s = segments[i]
        points[i] = s['Shape']['Points']

    return points