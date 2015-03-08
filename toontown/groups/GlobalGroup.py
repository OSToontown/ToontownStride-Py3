class GlobalGroup:

    def __init__(self, groupType, groupId):
        self.activePlayers = []
        self.groupType = groupType
        self.groupId = groupId

    def getGroupPlayers(self):
        return self.activePlayers

    def isInGroup(self, avId):
        if avId in self.activePlayers:
            return True
        return False

    def addPlayerToGroup(self, avId):
        self.activePlayers.append(avId)

    def removePlayerFromGroup(self, avId):
        self.activePlayers.remove(avId)
