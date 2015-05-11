from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.toon import ToonHead
from toontown.nametag import NametagGroup
from otp.otpbase import OTPGlobals

class DistributedJorElCam(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJorElCam')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.head = None
        self.dna = None

    def generate(self):
        DistributedObject.generate(self)
        self.dna = ToonDNA.ToonDNA()
        self.dna.newToonRandom()
        self.head = ToonHead.ToonHead()
        self.head.setupHead(self.dna)
        self.head.reparentTo(self.cr.playGame.hood.loader)
        self.head.setPos(75, 0, 20)
        self.head.setHpr(90, 0, 0)
        self.head.setScale(10)
        self.head.startBlink()
        self.head.startLookAround()

        pieces = [['*head*', '*muzzle*'], ['*ears*', '*nose*']]
        for p in pieces[0]:
            pc = '**/%s' % p
            for node in self.head.findAllMatches(pc):
                if not node.is_empty():
                    node.setColor(1, 1, 1, 1)
        for p in pieces[1]:
            pc = '**/%s' % p
            for node in self.head.findAllMatches(pc):
                if not node.is_empty():
                    node.setColor(0, 0, 0, 1)

        base.cr.jorElHead = self.head

    def delete(self):
        self.head.removeNode()
        self.head = None
        del base.cr.jorElHead
        DistributedObject.delete(self)

    def disable(self):
        self.head.removeNode()
        self.head = None
        del base.cr.jorElHead
        DistributedObject.disable(self)
