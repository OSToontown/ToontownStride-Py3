from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedGardenAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenAI")

    def __init__(self, air):
        self.air = air
        self.props = []

    def sendNewProp(self, prop, x, y, z):
        self.props.append([prop, x, y, z])
