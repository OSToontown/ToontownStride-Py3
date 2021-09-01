from direct.directnotify import DirectNotifyGlobal
from . import DistributedFactory

class DistributedFatalFactory(DistributedFactory.DistributedFactory):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFatalFactory')

    def __init__(self, cr):
        DistributedFactory.DistributedFactory.__init__(self, cr)

    def getFloorOuchLevel(self):
        return 8
