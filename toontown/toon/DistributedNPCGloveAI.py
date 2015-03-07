from DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from ToonDNA import ToonDNA
from toontown.toonbase import ToontownGlobals

class DistributedNPCGloveAI(DistributedNPCToonBaseAI):

    def requestTransformation(self, color):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if av is None or not hasattr(av, 'dna'):
            return
        
        if av.dna.gloveColor == color:
            self.sendUpdate('doTransformation', [avId, 1])
            return
        
        if av.getMoney() < ToontownGlobals.GloveCost:
            self.sendUpdate('doTransformation', [avId, 2])
            return

        av.takeMoney(ToontownGlobals.GloveCost)
        newDNA = ToonDNA()
        newDNA.makeFromNetString(av.getDNAString())
        newDNA.gloveColor = color
        taskMgr.doMethodLater(1.0, lambda task: av.b_setDNAString(newDNA.makeNetString()), 'transform-%d' % avId)
        self.sendUpdate('doTransformation', [avId, 3])