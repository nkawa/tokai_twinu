


class BaseAgent:
    def __init__(self,name):
        self.name = name
        self.x = 0
        self.y = 0
        self.z = 0
    
    def setPos(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def setSize(self,width,depth,height):
        self.width = width
        self.depth = depth
        self.height = height

    def rideOn(self, agent):
        self.is_riding = True
        self.on = agent
    
    def getOff(self, agent):
        self.is_riding = False
        if agent != self.on:
            print("Not get off from previous agent!!")
        self.on = None

