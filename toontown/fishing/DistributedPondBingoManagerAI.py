from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.fishing import BingoGlobals
from toontown.fishing import FishGlobals
from toontown.toonbase import ToontownGlobals
from toontown.fishing.NormalBingo import NormalBingo
from toontown.fishing.ThreewayBingo import ThreewayBingo
from toontown.fishing.DiagonalBingo import DiagonalBingo
from toontown.fishing.BlockoutBingo import BlockoutBingo
from toontown.fishing.FourCornerBingo import FourCornerBingo
from direct.task import Task
from direct.distributed.ClockDelta import *
import random, datetime
RequestCard = {}


class DistributedPondBingoManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPondBingoManagerAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.bingoCard = None
        self.tileSeed = None
        self.typeId = None
        self.state = 'Off'
        self.pond = None
        self.canCall = False
        self.shouldStop = False
        self.lastUpdate = globalClockDelta.getRealNetworkTime()
        self.cardId = 0

    def initTasks(self):
        now = datetime.datetime.now()
        weekday = now.weekday()
        targetday = 2 # Wednesday
        if weekday in (3, 4):
            targetday = 5
        togo = targetday - weekday
        if togo < 0:
            togo += 7
        s = now + datetime.timedelta(days=togo)
        start = datetime.datetime(s.year, s.month, s.day)
        secs = max(0, (start - now).total_seconds())
        self.notify.debug('Today it\'s %d, so we wait for %d, togo: %d %d' % (weekday, targetday, togo, secs))
        taskMgr.doMethodLater(secs, DistributedPondBingoManagerAI.startTask, self.taskName('start'), extraArgs=[self])

    def startTask(self):
        self.notify.debug('Starting game')

        def stop(task):
            self.notify.debug('Stopping game')
            self.shouldStop = True
            return task.done

        taskMgr.doMethodLater(24 * 60 * 60, stop, self.taskName('stop'))
        self.createGame()

    def setPondDoId(self, pondId):
        self.pond = self.air.doId2do[pondId]

    def getPondDoId(self):
        return self.pond.getDoId()

    def cardUpdate(self, cardId, cellId, genus, species):
        avId = self.air.getAvatarIdFromSender()
        spot = self.pond.hasToon(avId)
        if not spot:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to call bingo while not fishing!')
            return
        fishTuple = (genus, species)
        if (genus != spot.lastFish[1] or species != spot.lastFish[2]) and (spot.lastFish[0] != FishGlobals.BootItem):
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to update bingo card with a fish they didn\'t catch!')
            return
        if cardId != self.cardId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to update expired bingo card!')
            return
        if self.state != 'Playing':
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to update while the game is not running!')
            return
        spot.lastFish = [None, None, None, None]
        result = self.bingoCard.cellUpdateCheck(cellId, genus, species)
        if result == BingoGlobals.WIN:
            self.canCall = True
            self.sendCanBingo()
            self.sendGameStateUpdate(cellId)
        elif result == BingoGlobals.UPDATE:
            self.sendGameStateUpdate(cellId)

    def d_enableBingo(self):
        self.sendUpdate('enableBingo', [])

    def handleBingoCall(self, cardId):
        avId = self.air.getAvatarIdFromSender()
        spot = self.pond.hasToon(avId)
        if not spot:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to call bingo while not fishing!')
            return
        if not self.canCall:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to call bingo whle the game is not running!')
            return
        if cardId != self.cardId:
            self.air.writeServerEvent('suspicious', avId, 'Toon tried to call bingo with an expired cardId!')
            return
        av = self.air.doId2do[avId]
        av.d_announceBingo()
        self.rewardAll()

    def setJackpot(self, jackpot):
        self.jackpot = jackpot

    def d_setJackpot(self, jackpot):
        self.sendUpdate('setJackpot', [jackpot])

    def b_setJackpot(self, jackpot):
        self.setJackpot(jackpot)
        self.d_setJackpot(jackpot)

    def activateBingoForPlayer(self, avId):
        self.sendUpdateToAvatarId(avId, 'setCardState', [self.cardId, self.typeId, self.tileSeed, self.bingoCard.getGameState()])
        self.sendUpdateToAvatarId(avId, 'setState', [self.state, self.lastUpdate])
        self.canCall = True

    def sendStateUpdate(self):
        self.lastUpdate = globalClockDelta.getRealNetworkTime()
        for spot in self.pond.spots:
            if self.pond.spots[spot].avId == None or self.pond.spots[spot].avId == 0:
                continue
            avId = self.pond.spots[spot].avId
            self.sendUpdateToAvatarId(avId, 'setState', [self.state, self.lastUpdate])

    def sendCardStateUpdate(self):
        for spot in self.pond.spots:
            if self.pond.spots[spot].avId == None or self.pond.spots[spot].avId == 0:
                continue
            avId = self.pond.spots[spot].avId
            self.sendUpdateToAvatarId(avId, 'setCardState', [self.cardId, self.typeId, self.tileSeed, self.bingoCard.getGameState()])

    def sendGameStateUpdate(self, cellId):
        for spot in self.pond.spots:
            if self.pond.spots[spot].avId == None or self.pond.spots[spot].avId == 0:
                continue
            avId = self.pond.spots[spot].avId
            self.sendUpdateToAvatarId(avId, 'updateGameState', [self.bingoCard.getGameState(), cellId])

    def sendCanBingo(self):
        for spot in self.pond.spots:
            if self.pond.spots[spot].avId == None or self.pond.spots[spot].avId == 0:
                continue
            avId = self.pond.spots[spot].avId
            self.sendUpdateToAvatarId(avId, 'enableBingo', [])

    def rewardAll(self):
        self.state = 'Reward'
        self.sendStateUpdate()
        for spot in self.pond.spots:
            if self.pond.spots[spot].avId == None or self.pond.spots[spot].avId == 0:
                continue
            av = self.air.doId2do[self.pond.spots[spot].avId]
            av.addMoney(self.jackpot)
        if self.shouldStop:
            self.stopGame()
            return
        taskMgr.doMethodLater(5, DistributedPondBingoManagerAI.startWait, 'startWait%d' % self.getDoId(), [self])
        taskMgr.remove('finishGame%d' % self.getDoId())

    def finishGame(self):
        self.state = 'GameOver'
        self.sendStateUpdate()
        if self.shouldStop:
            self.stopGame()
            return
        taskMgr.doMethodLater(5, DistributedPondBingoManagerAI.startWait, 'startWait%d' % self.getDoId(), [self])

    def stopGame(self):
        self.state = 'CloseEvent'
        self.sendStateUpdate()
        taskMgr.doMethodLater(10, DistributedPondBingoManagerAI.turnOff, 'turnOff%d' % self.getDoId(), [self])

    def turnOff(self):
        self.state = 'Off'
        self.sendStateUpdate()

    def startIntermission(self):
        self.state = 'Intermission'
        self.sendStateUpdate()
        taskMgr.doMethodLater(300, DistributedPondBingoManagerAI.startWait, 'startWait%d' % self.getDoId(), [self])

    def startWait(self):
        self.state = 'WaitCountdown'
        self.sendStateUpdate()
        taskMgr.doMethodLater(15, DistributedPondBingoManagerAI.createGame, 'createGame%d' % self.getDoId(), [self])

    def createGame(self):
        self.canCall = False
        self.tileSeed = None
        self.typeId = None
        self.cardId += 1
        for spot in self.pond.spots:
            avId = self.pond.spots[spot].avId
            request = RequestCard.get(avId)
            if request:
                self.typeId, self.tileSeed = request
                del RequestCard[avId]
        if self.cardId > 65535:
            self.cardId = 0
        if not self.tileSeed:
            self.tileSeed = random.randrange(0, 65535)
        if self.typeId == None:
            self.typeId = random.randrange(0, 4)
        if self.typeId == BingoGlobals.NORMAL_CARD:
            self.bingoCard = NormalBingo()
        elif self.typeId == BingoGlobals.DIAGONAL_CARD:
            self.bingoCard = DiagonalBingo()
        elif self.typeId == BingoGlobals.THREEWAY_CARD:
            self.bingoCard = ThreewayBingo()
        elif self.typeId == BingoGlobals.FOURCORNER_CARD:
            self.bingoCard = FourCornerBingo()
        else:
            self.bingoCard = BlockoutBingo()
        self.bingoCard.generateCard(self.tileSeed, self.pond.getArea())
        self.sendCardStateUpdate()
        self.b_setJackpot(BingoGlobals.getJackpot(self.typeId))
        self.state = 'Playing'
        self.sendStateUpdate()
        taskMgr.doMethodLater(BingoGlobals.getGameTime(self.typeId), DistributedPondBingoManagerAI.finishGame, 'finishGame%d' % self.getDoId(), [self])
