import math

import mathfunctions
from chat_demo.settings import TRESHOLD_ANGLE, RADIUS
from gpsLocalization import data, myrepresentation
from gpsLocalization.myrepresentation import latlon2tuple
from mathfunctions import functions
from mathfunctions.functions import getAngleOfTwoSegments, dist2


def _getClosestEdge(point, edges):
    minDist = math.inf
    edgeMinDist = []
    for edge in edges:
        dist = distance2PointEdge(point,edge)
        if dist < minDist:
            minDist = dist
            edgeMinDist = edge

    return edgeMinDist


def locateMe(userPath):
    # estimate traveled segments
    paths = _getPathsNearby(userPath)
    usedEdges = _estimateTraveledEdges(userPath, paths)

    # estimate current position
    currentGpsPosition = userPath.getLastPosition()
    currentSegment = _getClosestEdge(currentGpsPosition,usedEdges)
    estimatedGpsPosition = _projectPointToSegment(currentGpsPosition, currentSegment)

    return estimatedGpsPosition, usedEdges


def _getLeastDistanceEdges(mapPaths, clustersForPaths, userPath):
    leastDistanceEdges = []
    leastDistance = math.inf
    # for each path
    for p_id in range(len(mapPaths)):
        # for each cluster
        path = mapPaths[p_id]
        clusters = clustersForPaths[p_id]

        for c_id in range(max(clusters)+1):
            # for each point traveled by user
            edges = getEdgesInCluster(c_id, clusters, path)
            nextEdges = getEdgesInCluster(c_id + 1, clusters, path)
            prevEdges = getEdgesInCluster(c_id - 1, clusters, path)

            dist = 0
            distNext = 0
            distPrev = 0

            for u in userPath.getBeforeCorner():
                dist += _distancePointEdges(u, edges)
            for u in userPath.getAfterCorner():
                distNext += _distancePointEdges(u, nextEdges)
                distPrev += _distancePointEdges(u, prevEdges)

            if distNext < distPrev:
                totalDistance = dist + distNext
                totalEdges = edges + nextEdges
            else:
                totalDistance = dist + distPrev
                totalEdges = edges + prevEdges

            if totalDistance < leastDistance:
                leastDistance = totalDistance
                leastDistanceEdges = totalEdges

    return leastDistanceEdges


def getEdgesInCluster(clusterId, clusters, path):
    edges = []
    for i in range(len(clusters)):
        if clusters[i] == clusterId:
            edges.append(_getEdge(i,path))

    return edges



def _estimateTraveledEdges(userPath, mapPaths):
    clustersForPaths = _clusterPaths(mapPaths)
    traveledEdges = _getLeastDistanceEdges(mapPaths,clustersForPaths, userPath)
    return traveledEdges


def _getPathsNearby(userPath):
    # get correct map data
    lat, lon = userPath.getCorner()
    radius = userPath.getRadius()

    paths = data.getPaths(lat, lon, radius)

    return paths


def _projectPointToSegment(last_position, last_traveled_segment):
    v = (last_traveled_segment[0]['Latitude'],
         last_traveled_segment[0]['Longitude'])

    w = (last_traveled_segment[1]['Latitude'],
        last_traveled_segment[1]['Longitude'])
    p = last_position
    projection = functions.project(v,w,p)
    return projection


def _clusterPaths(paths):
    """ for all paths: assign cluster to each edge of path"""
    n_g = len(paths)
    clusters = [[]] * n_g
    for i in range(n_g):
        clusters[i] = _clusterPath(paths[i])
    return clusters


def _clusterPath(sidewalk):
    # for one path: assign a cluster to each edge. Each cluster starts with angle 120 degrees or sharper

    n = len(sidewalk)-1
    labels = [0] * n
    START_LABEL = 0
    label = START_LABEL
    for i in range(n):
        # label segment
        labels[i] = label
        s = _getEdge(i, sidewalk)
        s_next = _getEdge(i + 1, sidewalk)

        if s_next == None:
            break

        #declare if next is from different cluster
        angle = getAngleOfTwoSegments(s, s_next)
        if angle < TRESHOLD_ANGLE:
            label+=1
        else:
            labels = _uniteLastWithFirst(START_LABEL, label, labels)


    return labels


def _getEdge(i, sidewalk):
    """ 
    Return an edge of a path represented by nodes [p1, p2, p3, p4, ...]
    The path can be closed or opened.
    """
    if i < len(sidewalk)-1:
        return sidewalk[i], sidewalk[i+1]
    else:
        if i < len(sidewalk):
            if i!=1 and sidewalk[i]==sidewalk[0]:
                return sidewalk[i],sidewalk[1]
        return None


def _uniteLastWithFirst(startLabel, endLabel, labels):
    n = len(labels)
    for i in reversed(range(n)):
        if labels[i] == endLabel:
            labels[i] = startLabel
        else:
            break
    return  labels


def _distancePointEdges(point, edges):
    """ return 2d distace between point (px,py) and array [(x1,y1), (...,...)] """
    d = math.inf
    for e in edges:
        d = min(d,distance2PointEdge(point,e))
    return d

def distance2PointEdge(p, segment):
    a = segment[0]
    b = segment[1]

    a_x = a['Latitude']
    a_y = a['Longitude']
    b_x = b['Latitude']
    b_y = b['Longitude']
    p_x = p[0]
    p_y = p[1]

    return dist2(a_x, a_y, b_x, b_y, p_x, p_y)


def getEdgesInPath(path):
    n = len(path)-1
    edges = [0]*n
    for i in range(n):
        edges[i] = (_getEdge(i,path))

    return edges

def getDistancePointPath(projection, path):
    edges = getEdgesInPath(path)
    return _distancePointEdges(projection, edges)


def _getPathForProjection(projection, paths):
    minPath = paths[0]
    minDistance = math.inf
    for path in paths:
        dist = getDistancePointPath(projection,path)
        if dist < minDistance:
            minDistance = dist
            minPath = path

    return minPath


def getClusterIdForProjection(clusters, path, projection_tuple):
    clusterId = clusters[0]
    minDist = math.inf
    for i in range(len(clusters)):
        edge = (_getEdge(i, path))
        dist = distance2PointEdge(projection_tuple, edge)

        if dist < minDist:
            minDist = dist
            clusterId = clusters[i]
    return clusterId


def getIdsForEdges(edges,nav_data):

    ids = []

    for long_segment in nav_data:
        simple_segments = getEdgesInPath(long_segment["Shape"]["Points"])
        id = long_segment["Id"]
        for segment in simple_segments:
            # todo set
            segment_a = segment[0]
            segment_b = segment[1]
            for edge in edges:
                e_a = edge[0]
                e_b = edge[1]
                if e_a == segment_a and e_b == segment_b:
                    ids.append(id)
                elif e_b == segment_a and e_a == segment_b:
                    ids.append(id)

    return ids


def getNearestEntryPoint(entrypoints, projection_tuple):
    minEntrypoint = entrypoints[0]
    minDist = math.inf
    for e in entrypoints:
        e_tuple = myrepresentation.latitudelongitude2tuple(e["Shape"])
        dist = mathfunctions.functions.length_squared(e_tuple, projection_tuple)
        if dist < minDist:
            minDist = dist
            minEntrypoint = e
    return minEntrypoint


def getEntryPointsForRoadIds(roadIds, nav_data):
    entryPoints = nav_data["AddressEntryPoints"]
    rememberedEntryPoints = []
    for entryPoint in entryPoints:
        for id in roadIds:
            if id == entryPoint["RoadId"]:
                rememberedEntryPoints.append(entryPoint)

    return rememberedEntryPoints


def getAddressForEntrypoint(nearest, nav_data):
    id = nearest["Id"]
    addresses = nav_data["Addresses"]
    my_address = {}
    for address in addresses:
        if address["Id"]== id:
            my_address = address
            break
    return my_address


def getAddressFromProjection(projection):
    lat = projection["lat"]
    lon = projection["lon"]
    nav_data_sidewalks = data.getSidewalkSegments(lat, lon, RADIUS+20)
    nav_data = data.getData(lat,lon,RADIUS+20)

    projection_tuple = latlon2tuple(projection)
    paths = _getPathsForProjection(projection)
    my_path = _getPathForProjection(projection_tuple,paths)
    clusters = _clusterPath(my_path)
    clusterLabel = getClusterIdForProjection(clusters, my_path, projection_tuple)
    edges = getEdgesInCluster(clusterLabel,clusters,my_path)
    roadIds = getIdsForEdges(edges,nav_data_sidewalks)
    entrypoints = getEntryPointsForRoadIds(roadIds,nav_data)
    nearest = getNearestEntryPoint(entrypoints,projection_tuple)
    address = getAddressForEntrypoint(nearest,nav_data)
    return address


def _getPathsForProjection(projection):
    lat = projection["lat"]
    lon = projection["lon"]
    radius = RADIUS
    paths = data.getPaths(lat, lon, radius)
    return paths
