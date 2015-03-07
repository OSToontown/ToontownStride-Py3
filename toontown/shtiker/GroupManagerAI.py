from pandac.PandaModules import *
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class GroupManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupManagerAI')

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.air = air
        self.shardGroups = {}

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        self.air.groupManager = self

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)
        self.air.groupManager = None

    def createGroup(self, shardId, playerId, groupType):
        if len(self.shardGroups[shardId]) is 0:
            groupId = 1
        else:
            groupId = sorted(self.shardGroups[shardId])[-1]+1
        if groupId in self.shardGroups[shardId]:
            return
        self.shardGroups[shardId][groupId] = [groupType, [playerId]]
        avId = self.air.getAvatarIdFromSender()
        groups = str(self.shardGroups)
        self.sendUpdateToAvatarId(avId, 'info', [groups])

    def closeGroup(self, shardId, groupId):
        if self.shardGroups[shardId].get(groupId):
            del self.shardGroups[shardId][groupId]
        avId = self.air.getAvatarIdFromSender()
        groups = str(self.shardGroups)
        self.sendUpdateToAvatarId(avId, 'info', [groups])

    def addPlayerId(self, shardId, groupId, playerId):
        if self.shardGroups[shardId].get(groupId) and playerId not in self.shardGroups[shardId].get(groupId):
            self.shardGroups[shardId][groupId][1].append(playerId)
        avId = self.air.getAvatarIdFromSender()
        groups = str(self.shardGroups)
        self.sendUpdateToAvatarId(avId, 'info', [groups])

    def removePlayerId(self, shardId, groupId, playerId):
        if self.shardGroups[shardId].get(groupId):
            self.shardGroups[shardId][groupId][1].remove(playerId)
        avId = self.air.getAvatarIdFromSender()
        groups = str(self.shardGroups)
        self.sendUpdateToAvatarId(avId, 'info', [groups])

    def getInfo(self, shardId):
        avId = self.air.getAvatarIdFromSender()
        groups = str(self.shardGroups)
        self.sendUpdateToAvatarId(avId, 'info', [groups])

    def setInfo(self, shardInfo):
        self.shardGroups = eval(shardInfo)
