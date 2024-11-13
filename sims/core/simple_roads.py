from numpy.random import randint
from truck import TruckAgent
import numpy as np
import math

def curve_points(start, end, control, resolution=5):
    	# If curve is a straight line
	if (start[0] - end[0])*(start[1] - end[1]) == 0:
		return [start, end]

	# If not return a curve
	path = []

	for i in range(resolution+1):
		t = i/resolution
		x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 *end[0]
		y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 *end[1]
		path.append((x, y))

	return path

def curve_road(start, end, control, resolution=15):
	points = curve_points(start, end, control, resolution=resolution)
	return [(points[i-1], points[i]) for i in range(1, len(points))]

TURN_LEFT = 0
TURN_RIGHT = 1
def turn_road(start, end, turn_direction, resolution=15):
	# Get control point
	x = min(start[0], end[0])
	y = min(start[1], end[1])

	if turn_direction == TURN_LEFT:
		control = (
			x - y + start[1],
			y - x + end[0]
		)
	else:
		control = (
			x - y + end[1],
			y - x + start[0]
		)
	
	return curve_road(start, end, control, resolution=resolution)


# 基本設定
n = 15   #分割数
a = 49   # 基本の y 側のshift   
b = 10
l = 50

# Nodes
WEST_RIGHT_START = (-b-l, a)
WEST_RIGHT_MID  = (-b, a)
EAST_RIGHT_MID  = (b, a)
EAST_RIGHT_END  = (b+l, a)

CENTER_POS = (0, a-b)
CENTER_STAY_POS = (0, a-b-4)

CENTER_POS2 = (-20, a-b)
CENTER_STAY_POS2 = (-20, a-b-4)



# Roads
WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT_MID)
CENTER_RIGHT = (WEST_RIGHT_MID, EAST_RIGHT_MID)
EAST_OUTBOUND = (EAST_RIGHT_MID, EAST_RIGHT_END)

NORTH_INBOUND = (CENTER_STAY_POS, CENTER_POS)
NORTH_EAST_CURVE = turn_road(CENTER_POS, EAST_RIGHT_MID, TURN_LEFT, n)

NORTH_INBOUND2 = (CENTER_STAY_POS2, CENTER_POS2)
NORTH_EAST_CURVE2 = turn_road(CENTER_POS2, WEST_RIGHT_MID, TURN_LEFT, n)



ROAD =  [
        WEST_INBOUND,
        CENTER_RIGHT,
        EAST_OUTBOUND,
        NORTH_INBOUND,
        *NORTH_EAST_CURVE,  # これも1つの道路
        NORTH_INBOUND2,
        *NORTH_EAST_CURVE2,
    ]

def getRoad(a, mv = np.array([3,0])):
    x = y = 0
    R = np.array([[np.cos(a), -np.sin(a)],
                [np.sin(a),np.cos(a)]])
    for p in ROAD:
        x += p[0][0]
        y += p[0][1]
    x /= len(ROAD)
    y /= len(ROAD)

    rds =[]
    for p in ROAD:
        res0 = np.dot(R, np.array(p[0]))+ mv
        res1 = np.dot(R, np.array(p[1]))+ mv
        rds.append((res0.tolist(),res1.tolist()))
    return rds

# 曲がる道路を一度に指定するハック
def road(a): return range(a, a+n)

#どんなトラック（経路）を出すかを指定する仕組み
trucks = [
    (1,{'path':[0,1,2]}),
    (1,{'path':[3,*road(4),2]}),
    (1,{'path':[3+n,*road(3+n),1,2]}),
]

# とりあえず5台最初に作っておく
NUM_TRUCKS = 5
truckAgents =[]
for i in range(0,NUM_TRUCKS):
    truckAgents.append(TruckAgent(i,1,2))



def getTruck():
    total = sum(pair[0] for pair in trucks)
    r = randint(1, total+1)
    for (weight, config) in trucks:
        r -= weight
        if r <= 0:
            for i in range(0,NUM_TRUCKS):
#                print("Truck",i,truckAgents[i].visible)
                if not truckAgents[i].visible:
                    truckAgents[i].visible= True
                    for attr, val in config.items():
                        setattr(truckAgents[i], attr, val)
                    return truckAgents[i]
    print("should not come here in getTruck")
    return None