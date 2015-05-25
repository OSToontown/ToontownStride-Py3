from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.toonbase import ToontownGlobals
from otp.speedchat import SpeedChatGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.hood import ZoneUtil
from pandac.PandaModules import Vec3

# Portable Hole settings
Hood2Details = {
    # hood : [pos, speedchatIndex, destination]
    2514: [(6, 7, 9), 109, 2514] # TTC, Hello?
}
Interior2Messages = {
    2514: ["Banker Bob: I have a very important message for you. Do not forget it.", "Banker Bob: Li0uLiAuLSAuLS0gLS4uLiAtLS0gLSAuLi4gLyAuLS4uIC0tLSAuLi4gLg=="]

}

class ARGManager(DistributedObjectGlobal):
    """
    This is a client-view of the manager that handles everything to do
    with the portable hole ARG event.
    """

    notify = directNotify.newCategory('ARGManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.setupPortableHoleEvent()

    def disable(self):
        self.cleanupPortableHoleEvent()
        DistributedObjectGlobal.disable(self)

    def delete(self):
        self.cleanupPortableHoleEvent()
        DistributedObjectGlobal.delete(self)

    def setupPortableHoleEvent(self):
        def phraseSaid(phraseId):
            if not hasattr(base.cr.playGame, 'place') or not base.cr.playGame.getPlace():
                return
            position, speedchatIndex, destination = Hood2Details.get(base.cr.playGame.getPlace().getZoneId(), [None, None, None])
            if not position or not speedchatIndex or not destination:
                return
            if speedchatIndex != phraseId:
                return
            msgBefore, msgAfter = Interior2Messages.get(destination, [None, None])
            if not msgBefore:
                self.notify.warning("Interior %d has no message definitions!" % destination)
                return
            taskMgr.doMethodLater(2, base.localAvatar.setSystemMessage, self.uniqueName("arg-before-msg"), extraArgs=[0, msgBefore])
            taskMgr.doMethodLater(7, base.localAvatar.setSystemMessage, self.uniqueName("arg-after-msg"), extraArgs=[0, msgAfter])
            if destination == 3823:
                taskMgr.doMethodLater(15, base.localAvatar.setSystemMessage, self.uniqueName("arg-after-after-msg"), extraArgs=[0, "'ttr://assets/LL-memo-607630003555.txt'. Keep it safe. I have no idea what it means, but Surlee certainly will."])
        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def cleanupPortableHoleEvent(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
