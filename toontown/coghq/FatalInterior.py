from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from .FactoryInterior import FactoryInterior

class FatalInterior(FactoryInterior):
    notify = DirectNotifyGlobal.directNotify.newCategory('FatalInterior')

    def __init__(self, loader, parentFSM, doneEvent):
        FactoryInterior.__init__(self, loader, parentFSM, doneEvent)
        self.zoneId = ToontownGlobals.SellbotFatalInt