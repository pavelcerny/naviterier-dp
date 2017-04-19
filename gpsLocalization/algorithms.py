def getFlagField(groupedSidewalks):
    ff = [[]]* len(groupedSidewalks)

    for i in range(len(groupedSidewalks)):
        ff[i] = [False]*(len(groupedSidewalks[i])-1)
    return ff


def getHittedSegments(grupedSidewalks, flagField, index):
    segments = []
    for i in range(len(flagField[index])):
        segment = {
            'a' : grupedSidewalks[index][i],
            'b' : grupedSidewalks[index][i+1],
        }
        segments.append(segment)

    return segments


def getLast(beforeCorner):
    lat = beforeCorner[-1]['lat']
    lon = beforeCorner[-1]['lon']
    return lat, lon


def splitInClusters(sidewalk, clusters):
    n_clusters = max(clusters)


