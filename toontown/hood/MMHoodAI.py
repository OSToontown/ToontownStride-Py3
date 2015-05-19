from toontown.hood import HoodAI
from toontown.safezone import DistributedTrolleyAI
from toontown.safezone import DistributedMMPianoAI
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedTrickOrTreatTargetAI

class MMHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.MinniesMelodyland,
                               ToontownGlobals.MinniesMelodyland)

        self.trolley = None
        self.piano = None

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()

        self.piano = DistributedMMPianoAI.DistributedMMPianoAI(self.air)
        self.piano.generateWithRequired(self.zoneId)    

        if simbase.air.wantHalloween:
            self.TrickOrTreatTargetManager = DistributedTrickOrTreatTargetAI.DistributedTrickOrTreatTargetAI(self.air)
            self.TrickOrTreatTargetManager.generateWithRequired(4835)

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()