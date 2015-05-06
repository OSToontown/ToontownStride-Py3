from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog.ClientServicesManagerUD import executeHttpRequestAndLog
import datetime
from direct.fsm.FSM import FSM
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from otp.ai.MagicWordGlobal import *
from direct.showbase.DirectObject import DirectObject

class BanFSM(FSM):

    def __init__(self, air, invokerId, avId, comment, duration):
        FSM.__init__(self, 'banFSM-%s' % avId)
        self.air = air
        self.invokerId = invokerId
        self.avId = avId
        self.comment = comment
        self.duration = duration
        self.DISLid = None
        self.accountId = None
        self.avName = None

    def performBan(self, bannedUntil):
        executeHttpRequestAndLog('ban', username=self.accountId, enddate=bannedUntil, comment=self.comment)

    def ejectPlayer(self):
        av = self.air.doId2do.get(self.avId)
        
        if not av:
            return

        datagram = PyDatagram()
        datagram.addServerHeader(
                av.GetPuppetConnectionChannel(self.avId),
                self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(103)
        simbase.air.send(datagram)

    def dbCallback(self, dclass, fields):
        if dclass != self.air.dclassesByName['AccountAI']:
            return

        self.accountId = fields.get('ACCOUNT_ID')

        if self.accountId:
            self.performBan(0 if self.duration < 0 else datetime.datetime.now() + (self.duration * 3600000))

    def getAvatarDetails(self):
        av = self.air.doId2do.get(self.avId)
        
        if not av:
            return

        self.DISLid = av.getDISLid()
        self.avName = av.getName()

    def log(self):
        simbase.air.writeServerEvent('ban', self.invokerId, self.accountId, self.comment)

    def cleanup(self):
        self.air = None
        self.avId = None
        self.DISLid = None
        self.avName = None
        self.invokerId = None
        self.accountId = None
        self.comment = None
        self.duration = None
        self = None

    def enterStart(self):
        self.getAvatarDetails()
        self.air.dbInterface.queryObject(self.air.dbId, self.DISLid, self.dbCallback)
        self.ejectPlayer()

    def exitStart(self):
        self.log()
        self.cleanup()

    def enterOff(self):
        pass

    def exitOff(self):
        pass


class BanManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerAI')

    def __init__(self, air):
        self.air = air
        self.banFSMs = {}

    def ban(self, invokerId, avId, duration, comment):
        self.banFSMs[avId] = BanFSM(self.air, invokerId, avId, comment, duration)
        self.banFSMs[avId].request('Start')

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.banDone, [avId])

    def banDone(self, avId):
        self.banFSMs[avId].request('Off')
        self.banFSMs[avId] = None


@magicWord(category=CATEGORY_MODERATOR, types=[str])
def kick(reason):
    """
    Kick the target from the game server.
    """
    target = spellbook.getTarget()
    invoker = spellbook.getInvoker()
    if target == invoker:
        return "You can't kick yourself!"
    datagram = PyDatagram()
    datagram.addServerHeader(
        target.GetPuppetConnectionChannel(target.doId),
        simbase.air.ourChannel, CLIENTAGENT_EJECT)
    datagram.addUint16(104)
    datagram.addString('You were kicked by a moderator for the following reason: "%s"\n\nBehave next time!' % reason)
    simbase.air.send(datagram)
    simbase.air.writeServerEvent('kick', invoker.doId, target.doId, reason)
    return "Kicked %s from the game server!" % target.getName()


@magicWord(category=CATEGORY_MODERATOR, types=[str, int])
def ban(reason, duration):
    """
    Ban the target from the game server.
    """
    target = spellbook.getTarget()
    invoker = spellbook.getInvoker()
    if target == invoker:
        return "You can't ban yourself!"
    simbase.air.banManager.ban(invoker.doId, target.doId, duration, reason)
    return "Banned %s from the game server!" % target.getName()
