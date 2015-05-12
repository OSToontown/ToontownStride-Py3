from pandac.PandaModules import *
from direct.distributed import ClockDelta
from toontown.chat.ChatGlobals import CFSpeech, CFTimeout
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toon import NPCToons
from DistributedNPCToonBase import DistributedNPCToonBase
import LaffRestockGlobals
from LaffShopGui import *

class DistributedNPCLaffRestock(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.laffGui = None

    def disable(self):
        self.ignoreAll()
        if self.laffGui:
            self.laffGui.destroy()
            self.laffGui = None
        self.av = None
        DistributedNPCToonBase.disable(self)

    def initToonState(self):
        self.setAnimState('neutral', 0.9, None, None)
        if self.name in NPCToons.LaffRestockPositions:
            pos = NPCToons.LaffRestockPositions[self.name]
            self.setPos(*pos[0])
            self.setH(pos[1])

    def getCollSphereRadius(self):
        return 1.25

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetLaffClerk(self):
        self.ignoreAll()
        if self.laffGui:
            self.laffGui.destroy()
            self.laffGui = None
        self.show()
        self.startLookAround()
        self.detectAvatars()
        if self.isLocalToon:
            self.showNametag2d()
            self.freeAvatar()
        return Task.done

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.SELL_MOVIE_CLEAR:
            return
        if mode == NPCToons.SELL_MOVIE_TIMEOUT:
            if self.isLocalToon:
                if self.laffGui:
                    self.laffGui.destroy()
                    self.laffGui = None
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetLaffClerk()
        elif mode == NPCToons.SELL_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                self.hideNametag2d()
                laff = self.av.getMaxHp() - self.av.getHp()
                cost = laff * ToontownGlobals.CostPerLaffRestock
                self.popupLaffGUI(laff, cost)
        elif mode == NPCToons.SELL_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.RestockLaffMessage, CFSpeech | CFTimeout)
            self.resetLaffClerk()
        elif mode == LaffRestockGlobals.FullLaff:
            self.setChatAbsolute(TTLocalizer.RestockFullLaffMessage, CFSpeech | CFTimeout)
            self.resetLaffClerk()
        elif mode == LaffRestockGlobals.NoMoney:
            self.setChatAbsolute(TTLocalizer.RestockNoMoneyMessage, CFSpeech | CFTimeout)
            self.resetLaffClerk()

    def __handleRestock(self, cost):
        self.sendUpdate('restock', [self.av.doId, cost])

    def __handleGuiDone(self, bTimedOut=False):
        self.ignoreAll()
        if self.laffGui:
            self.laffGui.destroy()
            self.laffGui = None
        if not bTimedOut:
            self.sendUpdate('transactionDone')

    def popupLaffGUI(self, laff, cost):
        self.setChatAbsolute('', CFSpeech)
        self.accept('restockLaff', self.__handleRestock)
        self.acceptOnce('guiDone', self.__handleGuiDone)
        self.laffGui = LaffShopGui(text=TTLocalizer.RestockAskMessage % (laff, cost),
                                   extraArgs=[cost])
