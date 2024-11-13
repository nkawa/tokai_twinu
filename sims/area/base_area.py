

# step chain
#   1. エリアマネージャが連携エリアと共通部分を共有
#   2. 


class BaseArea:
    def __init__(self, areaName):
        self.name = areaName
        self.agents = []

    def __str__(self):
        return self.name
    
    def addAgent(self,agent):
        self.agents.append(agent)
    
    def step(self,duration):
        for a in self.agents:
            a.step(duration)

    def getStates(self):
        states = []
        for a in self.agents:
            states.append(a.getState())
        return states


