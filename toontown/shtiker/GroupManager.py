from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class GroupManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.cr = cr
        self.groupStatus = {}

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.cr.groupManager = self
        self.d_getInfo(0)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        self.cr.groupManager = None

    def d_createGroup(self, shardId, playerId, groupType):
        self.sendUpdate('createGroup', [shardId, playerId, groupType])

    def d_closeGroup(self, shardId, groupId):
        self.sendUpdate('closeGroup', [shardId, groupId])

    def d_addPlayerId(self, shardId, groupId, playerId):
        self.sendUpdate('addPlayerId', [shardId, groupId, playerId])

    def d_removePlayerId(self, shardId, groupId, playerId):
        self.sendUpdate('removePlayerId', [shardId, groupId, playerId])

    def d_getInfo(self, shardId):
        self.sendUpdate('getInfo', [shardId])

    def d_setInfo(self, shardInfo):
        self.sendUpdate('setInfo', [shardInfo])

    def info(self, groups):
        self.groupStatus = eval(groups)
