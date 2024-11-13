from base_agent import BaseAgent
import random
import math

#トラックを表現するエージェント

class TruckAgent(BaseAgent):
    count = 0
    def __init__(self, ct, s1, s2, config={}):
        super().__init__("Truck"+str(ct).zfill(2))
        self.id = TruckAgent.count
        TruckAgent.count += 1
        self.s1 = s1
        self.s2 = s2
        self.setSize(2000, 2000, 2500)

        self.state = "stop"
        self.stateCount = 0
        self.visible = False  # 

        ## from Simulator Vehicle
        self.l = 6
        self.s0 = 6
        self.T = 1
        self.v_max = 16.6  # 速度
        self.a_max = 1.44  # 加速度
        self.b_max = 4.61

        self.sqrt_ab = 2*math.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

                # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)


    def step(self, lead, dt):
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0

        # 前に車がいた場合（障害物があった場合も同様に考えるべき）
        # 周辺エリア調査を行う仕組みを作るべき
        # 各エージェントは、エリアに前方車両の調査を依頼すべき
        # 自分の速度とduration で、調査すべきエリアの広さが気まる


        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max
        
    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max

    def setArea(self, ev_area):
        self.area = ev_area

    def remove(self):
        self.visible = False

# とりあえず使ってない
    def changeState(self):
        if self.state == "stop":
                if self.stateCount > self.s1:
                    self.state = "exit"            
                    self.targetDist = 10
                    self.dist = 0
                    self.currentSpeed = 1.5
                    self.stateCount = 0
                else:
                    self.stateCount += duration
        elif self.state == "exit":
                if self.dist < self.targetDist:
                    
                    self.dit = self.dist+ self.currentSpeed* duration
                else:
                    self.z = self.targetHeight
                    self.state = "stop1"
        elif self.state == "down":
                if self.z > self.targetHeight:
                    self.z = self.z - self.currentSpeed* duration
                else:
                    self.z = self.targetHeight
                    self.state = "stop"

        elif self.state == "stop1":
                if self.stateCount > self.s2:
                    self.state = "down"
                    self.targetHeight = 1
                    self.currentSpeed = 1.5
                    self.stateCount = 0
                else:
                    self.stateCount += duration

    def getState(self,area):
#        print ("getState",self.id,self.current_road_index, len(self.path), len(area.roads))

        road = area.roads[self.path[self.current_road_index]] 
        sin, cos = road.angle_sin, road.angle_cos
        x = road.start[0] + cos * (self.x) # - (self.l/2.0) )   # center
        y = road.start[1] + sin * (self.x) # - (self.l/2.0) )

        return {
            'type':'truck',
            'name':self.name, 
            'id': self.id,
            'cri': self.current_road_index,
#            'state':self.state,
#            'scount':self.stateCount,
            'speed':self.v,
            'pos': [x, y, 0, road.angle]
        }






