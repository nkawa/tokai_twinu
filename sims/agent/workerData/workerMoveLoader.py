#import json

import os
import pathlib
import math

#def LoadWorkerData(fname ="refMove.json"):
def LoadWorkerData(fname ="workerMove.json"):
    data = []
    centerX = 841/2
    centerY = 577/2
    scale = 0.101
    sx = 1
    sy = 10.5
    theta = -math.pi*6/180    # 6 degree
#    print("curret dir",os.getcwd(), pathlib.Path(__file__).parent.resolve())
    #ファイル名にパスがない場合は、このディレクトリにあると確認
    if os.path.basename(fname) == fname:
        path = pathlib.Path(__file__).parent.resolve()
        fname = os.path.join(path, fname)
    with open(fname) as file:
#        base = []
        for line in file:
            route = []
        #split
            pos = line.replace('[','').split(",")
            ln = len(pos)
            for i in range(0,ln-2,2):
                dx = (int(pos[i])-centerX)*scale
                dy = -(int(pos[i+1])-centerY)*scale
                x = sx-(dx*math.cos(theta)-dy*math.sin(theta) )
                y = sy -(dx*math.sin(theta)+dy*math.cos(theta) )
                route.append([x,y])
 #               base.append([int(pos[i]),int(pos[i+1])])
            data.append(route)   
            
    return data
#print ("Loaded", data)


#if __name__ == "__main__":
#    data, bs = LoadWorkerData()
#    print("Loaded", data )
#    print("bs", bs )