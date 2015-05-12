from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedGardenAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.props = []

    def generate(self):
        DistributedObjectAI.generate(self)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def disable(self):
        DistributedObjectAI.disable(self)

    def delete(self):
        DistributedObjectAI.delete(self)

    def b_setProps(self, props):
        self.setProps(props)
        self.d_setProps(props)

    def d_setProps(self, props):
        aProps = []
        for prop in props:
            aProps = aProps + prop
        self.sendUpdate('setProps', [aProps])

    def setProps(self, props):
        self.props = props
