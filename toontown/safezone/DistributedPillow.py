from panda3d.core import Point3, NodePath
from pandac.PandaModules import CollisionPolygon
from otp.otpbase import OTPGlobals
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm import ClassicFSM, State
from toontown.toonbase import ToontownGlobals

class DistributedPillow(DistributedObject):

    points = [
        Point3(-62.2896,  59.2746, -6.0),
        Point3(-119.969,  59.2746, -6.0),
        Point3(-67.1297,  55.2920, -1.6),
        Point3(-120.063,  55.2920, -1.6),
        Point3(-64.9566,  35.6930,  1.0),
        Point3(-119.993,  35.6930,  1.0),
        Point3(-63.4717,  0.00000,  1.6),
        Point3(-119.670,  0.00000,  1.6),
        Point3(-64.9566, -35.6930,  1.0),
        Point3(-119.993, -35.6930,  1.0),
        Point3(-67.1297, -55.2920, -1.6),
        Point3(-120.063, -55.2920, -1.6),
        Point3(-62.2896, -58.3746, -6.0),
        Point3(-119.969, -58.3746, -6.0),
        Point3(-104.100,  59.2746, -6.0),
        Point3(-104.100, -58.3746, -6.0),
        Point3(-104.100,  55.2920, -6.0),
        Point3(-104.100, -55.2920, -6.0),
    ]
    polygons = [[0, 1, 3, 2], [2, 3, 5, 4], [4, 5, 7, 6],
                [6, 7, 9, 8], [8, 9, 11, 10], [10, 11, 13, 12]]
    walls = [[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12],
             [3, 1], [5, 3], [7, 5], [9, 7], [11, 9], [13, 11],
             [3, 16], [17, 11], [16, 14], [15, 17]]

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.floorpolys = []
        self.wallpolys = []
        self.npaths = []
        self.np = None

    def generate(self):
        DistributedObject.generate(self)
        self.loader = self.cr.playGame.hood.loader
        self.np = NodePath('Pillow')
        self.np.reparentTo(render)
        for point in DistributedPillow.polygons:
            orderedPoints = []
            for index in point:
                orderedPoints.append(DistributedPillow.points[index])
            self.floorpolys.append(CollisionPolygon(*orderedPoints))
        for n, p in enumerate(self.floorpolys):
            polyNode = CollisionNode("FloorPoly-%d" % n)
            polyNode.addSolid(p)
            polyNode.setFromCollideMask(OTPGlobals.FloorBitmask)
            polyNodePath = self.np.attachNewNode(polyNode)
            self.npaths.append(polyNodePath)
            self.accept("enterFloorPoly-%d" % n, self.gravityHigh)
            self.accept("enterdonalds_dreamland", self.gravityLow)
        for wall in DistributedPillow.walls:
            ab = DistributedPillow.points[wall[0]]
            bb = DistributedPillow.points[wall[1]]
            cb = Point3(bb.getX(), bb.getY(), bb.getZ() + 20)
            db = Point3(ab.getX(), ab.getY(), ab.getZ() + 20)
            self.wallpolys.append(CollisionPolygon(ab, bb, cb, db))
        for n, p in enumerate(self.wallpolys):
            polyNode = CollisionNode("WallPoly-%d" % n)
            polyNode.addSolid(p)
            polyNode.setFromCollideMask(OTPGlobals.FloorBitmask)
            polyNodePath = self.np.attachNewNode(polyNode)
            self.npaths.append(polyNodePath)

    def disable(self):
        DistributedObject.disable(self)
        self.floorpolys = []
        self.wallpolys = []
        self.npaths = []
        if self.np:
            self.np.removeNode()
        self.np = None
        if hasattr(self, 'loader'):
            del self.loader

    def delete(self):
        if self.np:
            self.np.removeNode()
        self.np = None
        DistributedObject.delete(self)

    def gravityLow(self, entry):
        base.localAvatar.controlManager.currentControls.setGravity(ToontownGlobals.GravityValue * 1.25)

    def gravityHigh(self, entry):
        base.localAvatar.controlManager.currentControls.setGravity(ToontownGlobals.GravityValue * 2.00)
