import math
from copy import deepcopy

from scipy.spatial import distance
from collections import deque
from base_area import BaseArea

class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.angle = math.atan2(end[1]-start[1], end[0]-start[0])

        self.vehicles = deque()
        self.init_properties()

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal, group):
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

# 必ず先頭に信号があるという前提で道路ができている
# 道路には車両が順に入っている。
# 車線変更の概念は無いｗ
    def step(self, duration):
        n = len(self.vehicles)
        if n > 0:
            # Update first vehicle (別の道路のことも考慮すべき。（今はしてない)
            self.vehicles[0].step(None, duration)
            # Update other vehicles
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].step(lead, duration) # ここで問題は前の車しかみてないこと
                    # 近くの車や人も見るべき ⇒ 障害物検知
             # Check for traffic signal
            
            # 現時点では True/False で真偽のみ。本当は黄色も欲しい。
            # 道路端で止まってほしい時もダメ
            if self.traffic_signal_state:
                # If traffic signal is green or doesn't exist
                # Then let vehicles pass
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                # If traffic signal is red
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    # Slow vehicles in slowing zone
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._v_max)
                if self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and\
                   self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2:
                    # Stop vehicles in the stop zone
                    self.vehicles[0].stop()

# Road Area
class RoadArea(BaseArea):
    def __init__(self, config={}):
        # Set default configuration
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        self.generators = []
        self.traffic_signals = []
        self.dissapears = []    # Array to dissappear vehicles

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)
    
    def getStates(self):
        states = []
        for r in self.roads:
            for v in r.vehicles:
                states.append(v.getState(self))
        for v in self.dissapears:
            states.append({
            'type':'no-truck',
            'id': v.id,
            })
        self.dissapears = []
        return states


    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    
    def step(self,duration):
        # Update every road
        for road in self.roads:
            road.step(duration)

        # Add vehicles
        for gen in self.generators:
            gen.update()

        for signal in self.traffic_signals:
            signal.update(self)

        # Check roads for out of bounds vehicle
        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue
            # If not
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length: # その道路の端っこまで来てたら
                # If vehicle has a next road
                road.vehicles.popleft()  # まずは外す
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1              
                    vehicle.x = 0
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(vehicle)
                else: # no next road (dissapear)
                    vehicle.visible = False
                    vehicle.x = 0
                    vehicle.current_road_index = 0
#                    print("Add dissapear",vehicle.id, vehicle.x)
                    self.dissapears.append(vehicle)
                # In all cases, remove it from its road
        # Increment time
        self.t += self.dt
        self.frame_count += 1

