from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToontownGlobals import *

class GroupManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.shardGroups = {}
        self.groupPlayers = {}
        self.id2type = {
            SellbotHQ: 'VP Group',
            CashbotHQ: 'CFO Group',
            LawbotHQ: 'CJ Group',
            BossbotHQ: 'CEO Group',
        }

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.cr.groupManager = self
        self.d_setChildId()

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        self.cr.groupManager = None

    def d_setChildId(self):
        self.sendUpdate('setChildId', [])

    def isPlayerGrouped(self, avId):
        for group in self.groupPlayers.values():
            if avId in group:
                return True
        return False

    def isInGroup(self, avId, groupId):
        group = self.groupPlayers.get(groupId)
        if group is None:
            return False
        if avId in group:
            return True
        return False

    def requestInfo(self):
        self.sendUpdate('updateInfo', [])

    def getTypeFromId(self, groupId):
        return self.id2type.get(groupId)

    def setGroups(self, shardGroups):
        self.shardGroups = eval(shardGroups)

    def getGroups(self):
        return self.shardGroups

    def setGroupPlayers(self, groupPlayers):
        self.groupPlayers = eval(groupPlayers)

    def getGroupPlayers(self, groupId):
        group = self.groupPlayers.get(groupId)
        if group is None:
            return []
        return group

    def d_createGroup(self, groupId, groupType):
        self.sendUpdate('createGroup', [groupId, groupType])

    def d_closeGroup(self, groupId):
        self.sendUpdate('closeGroup', [groupId])

    def d_addPlayerToGroup(self, groupId, avId):
        self.sendUpdate('addPlayerToGroup', [groupId, avId])

    def d_removePlayerFromGroup(self, groupId, avId):
        self.sendUpdate('removePlayerFromGroup', [groupId, avId])
