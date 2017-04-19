import math

def minWithIdx(array):
    min = array[0]
    idx = 0
    for i in range(len(array)):
        if array[i] < min:
            min = array[i]
            idx = i
    return min, idx


# Return shortest squared distance of point p on a linesegment vw
def dist2(x1, y1, x2, y2, p_x, p_y):
    v = (x1,y1)
    w = (x2,y2)
    p = (p_x, p_y)

    projection = project(v,w,p)

    # return length(projection,p)
    return length_squared(projection,p)


# Return shortest projection of point p on a linesegment vw
def project(v,w,p):
    l2 = length_squared(v,w)

    # case v=w
    if l2 == 0:
        return v

    # Consider the line extending the segment, parameterized as v + t (w - v).
    # We find projection of point p onto the line.
    # It falls where t = [(p-v) . (w-v)] / |w-v|^2
    # We clamp t from [0,1] to handle points outside the segment vw.
    pv = minus(p, v)
    wv = minus(w, v)

    t = max(0, min(1, dot(pv, wv) / l2))

    projection_x = v[0] + t * (w[0] - v[0])
    projection_y = v[1] + t * (w[1] - v[1])
    projection = (projection_x,projection_y)
    return projection


# substract tuples
def minus(t1, t2):
    return t1[0]-t2[0], t1[1]-t2[1]

# dot product of tuples
def dot(t1, t2):
    return t1[0]*t2[0] + t1[1] * t2[1]

# squared length of tuples
def length_squared(v, w):
    dx = v[0]-w[0]
    dy = v[1]-w[1]
    return (dx*dx) + (dy*dy)

def length(v,w):
    return math.sqrt(length_squared(v,w))


def getAngleOfTwoSegments(s, t):
    v = ( s[1]['Latitude']-s[0]['Latitude'], s[1]['Longitude']-s[0]['Longitude'] )
    w = ( t[0]['Latitude']-t[1]['Latitude'], t[0]['Longitude']-t[1]['Longitude'] )

    angle = math.atan2(w[0], w[1]) - math.atan2(v[0],v[1])

    if (angle < 0):
        angle += 2 * math.pi

    angle = angle * 180 / math.pi

    if angle > 180:
        angle = 360 - angle

    return angle