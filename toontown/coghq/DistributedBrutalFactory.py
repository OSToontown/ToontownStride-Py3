from direct.directnotify import DirectNotifyGlobal
import DistributedFactory

class DistributedBrutalFactory(DistributedFactory.DistributedFactory):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBrutalFactory')

    def __init__(self, cr):
        DistributedFactory.DistributedFactory.__init__(self, cr)
    
    def getFloorOuchLevel(self):
        return 8
