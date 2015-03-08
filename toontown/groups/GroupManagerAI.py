from pandac.PandaModules import *
from direct.task import Task
from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToontownGlobals import *
from GlobalGroup import GlobalGroup

class GroupManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupManagerAI')

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.sellGroup = GlobalGroup('VP Group', SellbotHQ)
        self.cashGroup = GlobalGroup('CFO Group', CashbotHQ)
        self.lawGroup  = GlobalGroup('CJ Group', LawbotHQ)
        self.bossGroup = GlobalGroup('CEO Group', BossbotHQ)
        self.shardGroups = {
            SellbotHQ: self.sellGroup,
            CashbotHQ: self.cashGroup,
            LawbotHQ:  self.lawGroup,
            BossbotHQ: self.bossGroup,
        }
        self.groupPlayers = {
            SellbotHQ: [],
            CashbotHQ: [],
            LawbotHQ:  [],
            BossbotHQ: [],
        }
        self.id2type = {
            SellbotHQ: 'VP Group',
            CashbotHQ: 'CFO Group',
            LawbotHQ: 'CJ Group',
            BossbotHQ: 'CEO Group',
        }
        self.childId = None

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        self.air.groupManager = self
        self.confirmActiveToons = taskMgr.doMethodLater(30, self.confirmToonsInGroup, 'confirmActiveToons')

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)
        taskMgr.remove('confirmActiveToons')
        self.air.groupManager = None

    def setChildId(self):
        doId = self.air.getAvatarIdFromSender()
        self.childId = doId
        self.sendUpdateToAvatarId(self.childId, 'requestInfo', [])

    def isPlayerGrouped(self, avId):
        for group in self.shardGroups.values():
            if avId in group.getGroupPlayers():
                return True
        return False

    def isInGroup(self, avId, groupId):
        group = self.shardGroups.get(groupId)
        if group is None:
            return False
        if avId in group.getGroupPlayers():
            return True
        return False

    def confirmToonsInGroup(self, task):
        for groupId, group in self.groupPlayers.items():
            for player in group:
                toon = base.cr.doId2do.get(player)
                if toon.getZoneId() != groupId:
                    self.removePlayerFromGroup(groupId, player)
        return task.again

    def updateInfo(self):
        self.d_setGroupPlayers(str(self.groupPlayers))
        self.d_setGroups(str(self.id2type))

    def getTypeFromId(self, groupId):
        return self.id2type.get(groupId)

    def d_setGroups(self, shardGroups):
        self.sendUpdateToAvatarId(self.childId, 'setGroups', [shardGroups])

    def getGroups(self):
        return self.shardGroups

    def d_setGroupPlayers(self, groupPlayers):
        self.sendUpdateToAvatarId(self.childId, 'setGroupPlayers', [groupPlayers])

    def getGroupPlayers(self, groupId):
        group = self.shardGroups.get(groupId)
        if group is None:
            return []
        players = group.getGroupPlayers()
        return players

    def createGroup(self, groupId, groupType):
        group = self.shardGroups.get(groupId)
        if group is not None:
            newGroup = DistributedGlobalGroupAI(self.air, groupType, groupId)
            self.shardGroups.update(groupId, newGroup)
            players = {groupId: self.getGroupPlayers(groupId)}
            self.groupPlayers.update(players)
            self.updateInfo()

    def closeGroup(self, groupId):
        group = self.shardGroups.get(groupId)
        if group is not None:
            self.shardGroups.pop(groupId)
            self.groupPlayers.pop(groupId)
            self.updateInfo()

    def addPlayerToGroup(self, groupId, avId):
        group = self.shardGroups.get(groupId)
        if group is not None:
            if not group.isInGroup(avId):
                group.addPlayerToGroup(avId)
            players = {groupId: self.getGroupPlayers(groupId)}
            self.groupPlayers.update(players)
            self.updateInfo()

    def removePlayerFromGroup(self, groupId, avId):
        group = self.shardGroups.get(groupId)
        if group is not None:
            if group.isInGroup(avId):
                group.removePlayerFromGroup(avId)
            players = {groupId: self.getGroupPlayers(groupId)}
            self.groupPlayers.update(players)
            self.updateInfo()
