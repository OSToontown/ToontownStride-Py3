from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class AccountDateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("AccountDateAI")

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def requestDate(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        def callback(dclass, fields):
            if dclass is not None and dclass == self.air.dclassesByName['AccountAI'] and fields.has_key('CREATED'):
                self.sendUpdateToAvatarId(avId, 'requestDateResult', [fields.get('CREATED')])
            else:
                self.sendUpdateToAvatarId(avId, 'requestDateResult', [None])

        self.air.dbInterface.queryObject(self.air.dbId, av.DISLid, callback)
