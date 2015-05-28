from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm import ClassicFSM, State

class DistributedPillowAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def generate(self):
        DistributedObjectAI.generate(self)

    def delete(self):
        DistributedObjectAI.delete(self)
