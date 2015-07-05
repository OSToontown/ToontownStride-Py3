from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from datetime import datetime

class AccountDate(DistributedObject):
    neverDisable = 1
    notify = directNotify.newCategory('AccountDate')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.accountDays = 0

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        base.cr.accountDateMgr = self
        taskMgr.doMethodLater(10, self.requestDate, 'request-task')

    def delete(self):
        if hasattr(base.cr, 'accountDateMgr'):
            if base.cr.accountDateMgr is self:
                del base.cr.accountDateMgr
        DistributedObject.delete(self)

    def getAccountDays(self):
        return self.accountDays

    def requestDate(self, task=None):
        self.sendUpdate('requestDate')

        if task is not None:
            return task.done

    def requestDateResult(self, result):
        if result is None:
            notify.warning('Invalid response from server.')
            self.accountDays = 0
        else:
            date = datetime.strptime(result, "%a %b %d %H:%M:%S %Y")
            self.accountDays = (datetime.now() - date).days
