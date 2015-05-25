from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm import ClassicFSM, State

class DistributedPillowAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedPillowAI',
            [
                State.State('off', self.enterOff, self.exitOff,
                            ['bounce']),
                State.State('bounce', self.enterBounce, self.exitBounce,
                            ['off']),
            ], 'off', 'off')
        self.fsm.enterInitialState()

    def generate(self):
        DistributedObjectAI.generate(self)

    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        DistributedObjectAI.delete(self)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterBounce(self):
        pass

    def exitBounce(self):
        pass
