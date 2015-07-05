from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed import DistributedObjectAI


class DistributedBuildingQueryMgrAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('DistributedBuildingQueryMgrAI')

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.buildings = {}

    def isSuit(self, context, zoneId):
        avId = self.air.getAvatarIdFromSender()
        building = self.buildings.get(zoneId)
        if building is None:
            return
        self.sendUpdateToAvatarId(avId, 'response', [context, building.isSuitBlock()])
