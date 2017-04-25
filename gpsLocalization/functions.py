import math

from gpsLocalization import data
from mathfunctions.functions import getAngleOfTwoSegments, dist2
from mathfunctions import functions

TRESHOLD_ANGLE = 140

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