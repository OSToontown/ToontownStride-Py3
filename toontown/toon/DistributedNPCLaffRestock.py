from toontown.chat.ChatGlobals import CFSpeech, CFTimeout
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
from toontown.toon import NPCToons
from DistributedNPCToonBase import DistributedNPCToonBase
import LaffRestockGlobals

class DistributedNPCLaffRestock(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

    def disable(self):
        self.ignoreAll()
        self.destroyDialog()
        DistributedNPCToonBase.disable(self)

    def destroyDialog(self):
        if hasattr(self, 'dialog'):
            self.dialog.cleanup()
            del self.dialog
    
    def initToonState(self):
        self.setAnimState('neutral', 0.9, None, None)
        if self.name in NPCToons.LaffRestockPositions:
            pos = NPCToons.LaffRestockPositions[self.name]
            self.setPos(*pos[0])
            self.setH(pos[1])

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        laff = base.localAvatar.getMaxHp() - base.localAvatar.getHp()

        if laff <= 0:
            self.setChatAbsolute(TTLocalizer.RestockFullLaffMessage, CFSpeech|CFTimeout)
            return

        cost = laff * ToontownGlobals.CostPerLaffRestock

        if cost > base.localAvatar.getTotalMoney():
            self.setChatAbsolute(TTLocalizer.RestockNoMoneyMessage % cost, CFSpeech|CFTimeout)
            return

        base.cr.playGame.getPlace().setState('stopped')
        base.setCellsActive(base.bottomCells, 0)

        self.dialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=TTLocalizer.RestockAskMessage % (laff, cost), command=self.confirmRestock)
        self.dialog.show()

    def confirmRestock(self, value):
        base.cr.playGame.getPlace().setState('walk')
        base.setCellsActive(base.bottomCells, 1)

        if value > 0:
            self.sendUpdate('restock')
        else:
            self.setChatAbsolute(TTLocalizer.RestockLaffCancelMessage, CFSpeech|CFTimeout)

        self.destroyDialog()

    def restockResult(self, state, cost):
        if state == LaffRestockGlobals.NO_LAFF:
            message = TTLocalizer.RestockFullLaffMessage
        elif state == LaffRestockGlobals.NO_MONEY:
            message = TTLocalizer.RestockNoMoneyMessage % cost
        else:
            message = TTLocalizer.RestockLaffMessage

        self.setChatAbsolute(message, CFSpeech|CFTimeout)
