from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toon import ToonDNA

class DistributedJorElCamAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedJorElCamAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.dna = None

    def generate(self):
        self.dna = ToonDNA.ToonDNA()
        self.dna.newToonRandom()
        DistributedObjectAI.generate(self)

    def delete(self):
        del self.dna
        DistributedObjectAI.delete(self)

    def disable(self):
        self.dna = None
        DistributedObjectAI.disable(self)
