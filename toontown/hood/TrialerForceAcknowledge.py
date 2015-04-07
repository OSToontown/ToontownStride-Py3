from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import ZoneUtil
from toontown.toonbase import ToontownGlobals

class TrialerForceAcknowledge:

    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.dialog = None
        return

    def enter(self, destHood):
        doneStatus = {}

        def letThrough(self = self, doneStatus = doneStatus):
            doneStatus['mode'] = 'pass'
            messenger.send(self.doneEvent, [doneStatus])

        if not base.restrictTrialers:
            letThrough()
            return
        if base.roamingTrialers:
            letThrough()
            return
        if base.cr.isPaid():
            letThrough()
            return
        if ZoneUtil.getHoodId(destHood) in (ToontownGlobals.ToontownCentral, ToontownGlobals.MyEstate, ToontownGlobals.GoofySpeedway):
            letThrough()
            return
        else:
            try:
                base.localAvatar.b_setAnimState('neutral', 1)
            except:
                pass

        doneStatus['mode'] = 'fail'
        self.doneStatus = doneStatus

    def exit(self):
        if self.dialog:
            self.dialog.cleanup()
            self.dialog.unload()
            self.dialog = None
        return

    def handleOk(self):
        messenger.send(self.doneEvent, [self.doneStatus])
