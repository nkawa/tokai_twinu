import asyncio
import sys
import numpy as np

sys.path.append("sims/area/")
sys.path.append("sims/agent/")

import simple_roads 

from elevator import ElevatorAgent as Elevator
from elv_area import ElevatorArea
from floor_area import FloorArea
from road_area import RoadArea
from packet import PacketAgent 
from packet import AddPackets
from simple_worker import SimpleWorkerAgent
from simple_worker import AddWorkerAgents


class Engine():
    master = None
    def __init__(self,sio=None):
        self.sio = sio
        self.loop= False
        print("Engine",sio)
        Engine.master = self
        self.areas = []
        self.upcoming_vehicle = simple_roads.getTruck()  # 事前に追加するトラックを用意
        self.roadArea = None
    
    def addArea(self,a):
        self.areas.append(a)    

    def stop(self):
        self.loop = False

    def addTruck(self):
        if self.upcoming_vehicle == None:
            self.upcoming_vehicle =  simple_roads.getTruck()
            if self.upcoming_vehicle == None:
                print("Can't add new Truck!")
                return
        road = self.roadArea.roads[self.upcoming_vehicle.path[0]]      
        if len(road.vehicles) == 0 \
            or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.l:
                # If there is space for the generated vehicle; add it
            road.vehicles.append(self.upcoming_vehicle)
            self.upcoming_vehicle =  simple_roads.getTruck()  #random truck..
        # can't add vehicle because of space..
    
        

    async def showRoads(self):
        print("Show roads!", len(self.roadArea.roads))
        states = []
        for i,r in enumerate(self.roadArea.roads):
            states.append(
                {            
                    'type':'road',
                    'id': i,
                    'pos': [r.start,r.end]
                }
            )
        await asyncio.wait([asyncio.create_task(self.sio.emit('events',states))])

    async def run(self,sio,duration, speed = 1):
        self.loop = True
        while self.loop:
            for a in self.areas:
                a.step(duration)
            states = []
            for a in self.areas:
                s = a.getStates()  
                states.extend(s)
            await asyncio.wait([asyncio.create_task(sio.emit('events',states))])
#            print("Send Events!",states)
            await asyncio.sleep(duration/speed)
        print("Engine stopped")


# need to be singletone!
async def doit(sio):
    print("called from web!",sio)
    if Engine.master == None:
        e = Engine(sio)
        evarea = ElevatorArea("Ea1")
        e1 = Elevator(1,3,7)
        e2 = Elevator(2,5,6)
        evarea.addAgent(e1)
        evarea.addAgent(e2)
        e.addArea(evarea)

        e.roadArea = RoadArea()
        e.roadArea.create_roads(simple_roads.getRoad(np.pi*6/180))
        
        e.addArea(e.roadArea)
        # add packets
        floor = FloorArea("Floor3F")
        AddPackets(floor)
        
        AddWorkerAgents(floor)
        
        e.addArea(floor)
    else:
        e = Engine.master
    
    if not e.loop: 
        await e.run(sio, duration = 0.1, speed= 1)

async def addPacket():
    if Engine.master != None:
        Engine.master.addPacket()

async def addTruck():
    if Engine.master != None:
        Engine.master.addTruck()
async def showRoads():
    print("Show roadsEV")
    if Engine.master != None:
        await Engine.master.showRoads()


async def stop(sio):
    print("called from web!",sio)
    Engine.master.stop()
