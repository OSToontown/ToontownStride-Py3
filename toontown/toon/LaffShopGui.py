from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
from toontown.toontowngui import TTDialog
import LaffRestockGlobals

class LaffShopGui(object, DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('LaffShopGui')

    def __init__(self, **kw):
        self.dialog = None
        self.timer = None
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(aspect2d)
        self.timer.posInTopRightCorner()
        self.timer.accept('RESET_LAFFSHOP_TIMER', self.__resetTimer)
        self.timer.countdown(LaffRestockGlobals.LAFFCLERK_TIMER, self.__timerExpired)
        self.__doDialog(**kw)

    def destroy(self):
        self.ignoreAll()
        if self.timer:
            self.timer.destroy()
        self.timer = None
        if self.dialog:
            self.dialog.destroy()
        self.dialog = None

    def __resetTimer(self):
        if self.timer:
            self.timer.stop()
            self.timer.countdown(LaffRestockGlobals.LAFFCLERK_TIMER, self.__timerExpired)

    def __timerExpired(self):
        messenger.send('guiDone', [True])

    def __destroyDialog(self, resp, cost):
        if self.timer:
            self.ignoreAll()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        if resp == LaffRestockGlobals.Success:
            messenger.send('restockLaff', [cost])
        messenger.send('guiDone', [False])

    def __doDialog(self, **kw):
        self.dialog = TTDialog.TTDialog(style=TTDialog.YesNo,
                                        command=self.__destroyDialog,
                                        **kw)
        self.dialog.show()
