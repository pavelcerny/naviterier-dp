from gpsLocalization import myrepresentation
from apis import naviterier_api


def getSegments(lat, lon, radius):
    segments = naviterier_api.findSegments(lat, lon, radius)

    return segments


def getSidewalkSegments(lat, lon, radius):
    segments = naviterier_api.findSegments(lat, lon, radius, "Sidewalk")

    return segments


def getPaths(lat, lon, radius):
    segments = getSidewalkSegments(lat,lon,radius)
    points = myrepresentation.naviterierSegments2points(segments)
    paths = _mergePaths(points)
    return paths


def _mergePaths(paths):
    """ merge each 2 paths with the same ending/starting point """
    n_groups = len(paths)
    while True:
        paths = _mergePathsOneStep(paths)
        if len(paths) == n_groups:
            break
        else:
            n_groups = len(paths)
    return paths


def _mergePathsOneStep(paths):
    """ one step of merging each 2 paths with the same ending/starting point"""
    groups = []
    # add first
    first = paths[0]
    rest = paths[1:]
    groups.append(first)

    for s in rest:
        createNew = True

        # sort into correct group
        for i in range(0, len(groups)):
            # start == start
            if groups[i][0] == s[0]:
                # reverse s
                rev_s = s[::-1]
                # prepend without last
                groups[i] = rev_s[:-1] + groups[i]
                createNew = False
                break
            # start == end
            elif groups[i][0] == s[-1]:
                # prepend without last
                groups[i] = s[:-1] + groups[i]
                createNew = False
                break
            # end == start
            elif groups[i][-1] == s[0]:
                # append without first
                groups[i] = groups[i] + s[1:]
                createNew = False
                break
            # end == end
            elif groups[i][-1] == s[-1]:
                # reverse s
                rev_s = s[::-1]
                # append without first
                groups[i] = groups[i] + rev_s[1:]
                createNew = False
                break
        # begin new group
        if createNew:
            groups.append(s)

    return groups