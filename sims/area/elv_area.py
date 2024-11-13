from base_area import BaseArea

class ElevatorArea(BaseArea):

    def step(self,duration):
        for a in self.agents:
            a.step(duration)




    