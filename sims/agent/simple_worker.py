from base_agent import BaseAgent
from workerData.workerMoveLoader import LoadWorkerData
import random
import math

# シンプルな作業者エージェント
# 移動のルーティングは別ファイルで作成済みとする
# そのファイルを読み込んで動作する


def AddWorkerAgents(floor):
    moves = LoadWorkerData()
    count = 1
    for move in moves:
        ag = SimpleWorkerAgent(count, move, 19.0)
        floor.addAgent(ag)
        count += 1


class SimpleWorkerAgent(BaseAgent):
    count = 0
    moveScale = 1.0   # 移動距離を計算
    # 単純に move の位置を往復するだけの agent
    # state は walk -> rwalk の2種類

    def __init__(self, ct, move, z):
        #        print("init agent ",ct)
        super().__init__("Worker"+str(ct).zfill(4))
        self.id = SimpleWorkerAgent.count
        SimpleWorkerAgent.count += 1
        self.move = move
        self.x = move[0][0] * SimpleWorkerAgent.moveScale
        self.y = move[0][1] * SimpleWorkerAgent.moveScale
        self.z = z
        self.angle = 0
        self.setSize(20, 20, 20)
        self.sentMoves = False

        self.state = "walk"
        self.stateCount = 0
        self.stateTime = 0
        self.speedScale = 8 + random.randint(0,6) # 20    # duration が 1 で 移動量が 5Count 移動する、とする。
        self.stopped = False


# worker の現在位置を計算

    def step(self, duration):  # devide position using duration
        lastCount = self.stateCount
        dt = 0
        self.stateTime += duration * self.speedScale
        nextCount = int(self.stateTime) + 1
        if lastCount != int(self.stateTime):  # もし次以後のステートにいった場合は？
            if nextCount >= len(self.move):
                #state change                
                nextCount = 1
                lastCount = 0
                self.stateTime %= 1
                self.stateCount = 0
                if self.state == "walk":
                    self.state = "rwalk"  # rwalk is reverse walk for the route.
                else:
                    self.state = "walk"
            else:
                self.stateCount = int(self.stateTime)
                lastCount = self.stateCount
        dt = self.stateTime - lastCount
        if self.state == "rwalk":
            lastCount = len(self.move)-lastCount-1
            nextCount = len(self.move)-nextCount-1
        dx = (self.move[nextCount][0]-self.move[lastCount][0])
        dy = (self.move[nextCount][1]-self.move[lastCount][1])
        self.angle = math.atan2(-dx, dy)

        if self.id == 1:
            print("DXD:", lastCount, "nx:", nextCount,self.state,":",dt,dx,dy,"angle:", self.angle)
        self.x = self.move[lastCount][0]+dx*dt
        self.y = self.move[lastCount][1]+dy*dt

    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def setArea(self, ev_area):
        self.area = ev_area

    def remove(self):
        self.visible = False

    def getState(self):
        #        if self.id < 1:
        #            print ("getStateAgent",self.id,self.name, self.x, self.y, self.state, self.stateCount, self.stateTime)
        pos = [self.x, self.y, self.z, self.angle]
        if not self.sentMoves:   # 初回だけ、移動経路も送っちゃう！　（これは simple worker 特別）
            pos.append(self.move)
            self.sentMoves= True
        return {
            'type': 'worker',
            'name': self.name,
            'id': self.id,
            'pos':pos
        }
