from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedLobbyManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLobbyManagerUD")

    def announceGenerate(self):
        DistributedObjectUD.announceGenerate(self)
        self.sendUpdate('lobbyManagerUdStartingUp')
