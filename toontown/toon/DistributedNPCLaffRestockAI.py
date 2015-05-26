from direct.distributed import ClockDelta
from toontown.toonbase import ToontownGlobals
from DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.task import Task
import LaffRestockGlobals
from toontown.toon import NPCToons
from DistributedToonAI import DistributedToonAI

zone2id = {
    10000: 0,
    13000: 1,
    12000: 2,
    11000: 3,
}

class DistributedNPCLaffRestockAI(DistributedNPCToonBaseAI):

    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        self.givesQuests = 0
        self.busy = 0

    def generate(self):
        DistributedToonAI.generate(self)
        self.b_setCogIndex(zone2id[self.zoneId])

    def delete(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.ignoreAll()
        DistributedNPCToonBaseAI.delete(self)

    def d_setMovie(self, avId, flag, extraArgs=[]):
        self.sendUpdate('setMovie', [flag,
         self.npcId,
         avId,
         extraArgs,
         ClockDelta.globalClockDelta.getRealNetworkTime()])

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if avId not in self.air.doId2do:
            self.notify.warning('Avatar: %s not found' % avId)
            return
        if self.isBusy():
            self.freeAvatar(avId)
            return
        av = self.air.doId2do[avId]
        self.busy = avId
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])
        laff = av.getMaxHp() - av.getHp()
        cost = laff * ToontownGlobals.CostPerLaffRestock
        if laff <= 0:
            self.d_setMovie(avId, LaffRestockGlobals.FullLaff)
            self.sendClearMovie(None)
        elif cost > av.getTotalMoney():
            self.d_setMovie(avId, LaffRestockGlobals.NoMoney)
            self.sendClearMovie(None)
        else:
            self.d_setMovie(avId, NPCToons.SELL_MOVIE_START)
            taskMgr.doMethodLater(LaffRestockGlobals.LAFFCLERK_TIMER, self.sendTimeoutMovie, self.uniqueName('clearMovie'))
            DistributedNPCToonBaseAI.avatarEnter(self)

    def transactionDone(self):
        avId = self.air.getAvatarIdFromSender()
        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCLaffRestockAI.transactionDone busy with %s' % self.busy)
            self.notify.warning('somebody called transactionDone that I was not busy with! avId: %s' % avId)
            return
        av = simbase.air.doId2do.get(avId)
        if av:
            self.d_setMovie(avId, NPCToons.SELL_MOVIE_COMPLETE, [])
        self.sendClearMovie(None)
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.sendClearMovie(None)
        return

    def sendTimeoutMovie(self, task):
        self.d_setMovie(self.busy, NPCToons.SELL_MOVIE_TIMEOUT)
        self.sendClearMovie(None)
        return Task.done

    def sendClearMovie(self, task):
        self.ignore(self.air.getAvatarExitEvent(self.busy))
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.busy = 0
        self.d_setMovie(0, NPCToons.SELL_MOVIE_CLEAR)
        return Task.done

    def restock(self, avId, laff, cost):
        sendAvId = self.air.getAvatarIdFromSender()
        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCLaffRestockAI.restock busy with %s' % self.busy)
            self.notify.warning('somebody called restock that I was not busy with! avId: %s' % avId)
            return
        av = simbase.air.doId2do.get(avId)
        if av:
            if av.getMaxHp() < (av.getHp() + laff):
                movieType = NPCToons.SELL_MOVIE_CHEATER
                self.air.writeServerEvent('suspicious', avId, 'DistributedNPCLaffRestockAI.restock invalid restock')
                self.notify.warning('somebody tried to buy an invalid hp restock! avId: %s' % avId)
            else:
                movieType = NPCToons.SELL_MOVIE_COMPLETE
                av.takeMoney(cost)
                av.b_setHp(av.getHp() + laff)
