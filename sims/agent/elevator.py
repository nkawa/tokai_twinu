
from base_agent import BaseAgent
import random

#エレベータを表現するエージェント

class ElevatorAgent(BaseAgent):
    def __init__(self, ct,s1,s2):
        super().__init__("Elevator"+str(ct).zfill(2))
        self.id = ct-1  # ct might be 1,2... 
        self.s1 = s1
        self.s2 = s2
        self.setSize(2000, 2000, 2500)
        self.maxSpeed = 3      #  3m/sec
        self.acceleration = 1  # 1m/s^2
        self.currentSpeed = 0
        self.targetHeight = 0
        self.state = "stop"
        self.stateCount = 0


    def setArea(self, ev_area):
        self.area = ev_area

    def step(self,duration):
        if self.state == "stop":
                if self.stateCount > self.s1:
                    self.state = "up"                    
                    self.targetHeight = 9+ random.randint(0,1)*9
                    self.currentSpeed = 1.5
                    self.stateCount = 0
                else:
                    self.stateCount += duration
        elif self.state == "up":
                if self.z < self.targetHeight:
                    self.z = self.z+ self.currentSpeed* duration
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
                    self.targetHeight = 0
                    self.currentSpeed = 1.5
                    self.stateCount = 0
                else:
                    self.stateCount += duration

    def getState(self):
        return {
            'type':'elv',
            'id':self.id, 
            'state':self.state,
            'scount':self.stateCount,
            'pos': [self.x, self.y, self.z]
        }






