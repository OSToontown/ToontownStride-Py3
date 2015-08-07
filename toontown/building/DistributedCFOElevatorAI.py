from ElevatorConstants import *
import DistributedBossElevatorAI

class DistributedCFOElevatorAI(DistributedBossElevatorAI.DistributedBossElevatorAI):

    def __init__(self, air, bldg, zone, antiShuffle = 0):
        DistributedBossElevatorAI.DistributedBossElevatorAI.__init__(self, air, bldg, zone, antiShuffle=antiShuffle)
        self.type = ELEVATOR_CFO
        self.countdownTime = ElevatorData[self.type]['countdown']
