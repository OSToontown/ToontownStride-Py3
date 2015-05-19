from direct.distributed import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class GroupManagerUD(DistributedObjectUD.DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupManagerUD')

    def __init__(self, air):
        DistributedObjectUD.DistributedObjectUD.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectUD.DistributedObjectUD.announceGenerate(self)

    def delete(self):
        DistributedObjectUD.DistributedObjectUD.delete(self)
