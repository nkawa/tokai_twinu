
from base_agent import BaseAgent
import random
import math

packetloc = [
"6.64130210876 3.90407395363 -0.369742006063",
"5.81450653076 -2.09599590302 -0.8615000844",
"6.6485042572 3.01742506027 -1.29950523376",
"5.50717926025 -2.29648709297 -0.781618475914",
"6.30996894836 3.36792612076 -1.38713145256",
"5.77131128311 -0.548538982868 -0.573678553104",
"6.80605602264 3.18647146225 -1.05291974545",
"6.49840259552 3.30610752106 -1.22821164131",
"4.23960494995 -0.89044046402 -0.605436563492",
"5.32149791718 -2.57702732086 -0.900920987129",
"5.4522228241 -2.04600191116 -0.985978245735",
"5.60296297073 -1.05627095699 -0.537142515182",
"5.36525630951 -2.92283391953 -1.08855247498",
"4.46727848053 -0.556627333164 -0.592173814774",
"6.88975048065 2.93030786514 -1.23387241364",
"4.17373371124 -1.24203753471 -0.910922646523",
"4.4733505249 -3.30228304863 -1.10714411736",
"4.0404958725 -0.848483860493 -0.897724032402",
"5.83563232422 -2.63950061798 -0.53967499733",
"4.57867527008 -0.564073324203 -0.58426296711",
"7.18623590469 -1.69655179977 -0.482377052307",
"5.39195632935 -2.54636049271 -0.800388336182",
"6.52876567841 3.2339348793 -1.27782011032",
"4.13141155243 -1.17761063576 -0.889313817024",
"6.85659408569 2.97550320625 -1.25191342831"]
#//1640146978241994066


# this is only for small demo.
def AddPackets(floor):
    i = 1    
    for item in packetloc:
        pos = item.split()
        x = float(pos[0])
        y = -float(pos[1])
        z = float(pos[2])
        ag = PacketAgent(i,x,y,z)
        i+= 1
        floor.addAgent(ag)
        

class PacketAgent(BaseAgent):
    count = 0
    def __init__(self, ct, x, y, z, config={}):
#        print("init packet ",ct)
        super().__init__("Packet"+str(ct).zfill(4))
        self.id = PacketAgent.count
        PacketAgent.count += 1
        self.x = x
        self.y = y
        self.z = z
        self.setSize(20, 20, 25) 

        self.state = "stop"
        self.stateCount = 0
        self.visible = False  # 

        self.path = []
        self.stopped = False

                # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)


    def step(self, duration):
        pass # do noting.
        
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

    def getState(self):
#        print ("getStatePacket",self.id,self.name)
        return {
            'type':'packet',
            'name':self.name, 
            'id': self.id,
            'pos': [self.x, self.y, self.z, 0]
        }







