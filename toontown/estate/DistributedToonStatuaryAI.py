from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI

class DistributedToonStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonStatuaryAI")

    def __init__(self, air, species, dnaCode):
        self.air = air
        self.species = species
        self.dnaCode = dnaCode

    def setOptional(self, opt):
        self.optional = opt
