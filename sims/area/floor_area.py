from base_area import BaseArea
import csv


class FloorArea(BaseArea):
    def __init__(self, floorName):
        super(FloorArea, self).__init__(floorName)
        print("Floor init",floorName)
        
#        reader = csv.reader("poses.csv")
#        self.rows = []
#        row_count = 0
#        for i, row in enumerate(reader):
#            if i % 10 == 0:
#                self.rows.append(row)
#                row_count += 1
                
    def step(self,duration):
        for a in self.agents:
            a.step(duration)




    