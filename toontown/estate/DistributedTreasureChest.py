from direct.distributed.DistributedObject import DistributedObject
from pandac.PandaModules import *
from toontown.fishing import FishSellGUI
from toontown.toonbase import ToontownGlobals, TTLocalizer
import TreasureChestGlobals

class DistributedTreasureChest(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr = cr
        self.createModel(45, -165.75, 0.025, 30)
        self.initCollisions()

    def delete(self):
        self.ignore('enter' + self.cSphereNode.getName())
        self.cSphereNodePath.removeNode()
        self.model.removeNode()
        self.destroyFishGui()
        del self.cSphere
        del self.cSphereNode
        del self.cSphereNodePath
        del self.model
        DistributedObject.delete(self)

    def destroyFishGui(self):
        self.ignore('treasureChestSell')

        if hasattr(self, 'fishGui'):
            self.fishGui.destroy()
            del self.fishGui

    def createModel(self, x, y, z, h):
        self.model = loader.loadModel('phase_4/models/minigames/treasure_chest.bam')
        self.model.reparentTo(render)
        self.model.setScale(1.5)
        self.model.setPos(x, y, z)
        self.model.setH(h)

    def initCollisions(self):
        self.cSphere = CollisionTube(0.0, 1.0, 0.0, 0.0, 1.0, 5.0, ToontownGlobals.TreasureChestSphereRadius)
        self.cSphere.setTangible(0)
        self.cSphereNode = CollisionNode('cSphereNode')
        self.cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.model.attachNewNode(self.cSphereNode)
        self.cSphereNodePath.hide()
        self.cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.accept('enter' + self.cSphereNode.getName(), self.handleCollisionSphereEnter)

    def handleCollisionSphereEnter(self, collEntry):
        if not base.localAvatar.fishTank.getFish():
            base.localAvatar.setSystemMessage(0, TTLocalizer.STOREOWNER_NOFISH)
            return

        base.setCellsActive(base.bottomCells, 0)
        base.cr.playGame.getPlace().setState('stopped')
        self.acceptOnce('treasureChestSell', self.handleSaleDone)
        self.fishGui = FishSellGUI.FishSellGUI('treasureChestSell')

    def handleSaleDone(self, sell):
        self.destroyFishGui()
        base.setCellsActive(base.bottomCells, 1)
        base.cr.playGame.getPlace().setState('walk')
        self.sendUpdate('completeSale', [sell])

    def completeSaleResult(self, state, numFish, maxFish):
        if state == TreasureChestGlobals.TROPHY:
            base.localAvatar.setSystemMessage(0, TTLocalizer.STOREOWNER_TROPHY % (numFish, maxFish))
        elif state == TreasureChestGlobals.COMPLETE:
            base.localAvatar.setSystemMessage(0, TTLocalizer.STOREOWNER_THANKSFISH)
        elif state == TreasureChestGlobals.NONE:
            base.localAvatar.setSystemMessage(0, TTLocalizer.STOREOWNER_NOFISH)
