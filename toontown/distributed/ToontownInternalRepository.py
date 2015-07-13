from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownNetMessengerAI import ToontownNetMessengerAI
from direct.distributed.PyDatagram import PyDatagram
import traceback
import sys

class ToontownInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames=None,
                 dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(
            self, baseChannel, serverId=serverId, dcFileNames=dcFileNames,
            dcSuffix=dcSuffix, connectMethod=connectMethod, threadedNet=threadedNet)
    
    def handleConnected(self):
        self.__messenger = ToontownNetMessengerAI(self)
    
    def sendNetEvent(self, message, sentArgs=[]):
        self.__messenger.send(message, sentArgs)
        
    def addExitEvent(self, message):
        dg = self.__messenger.prepare(message)
        self.addPostRemove(dg)
        
    def handleDatagram(self, di):
        msgType = self.getMsgType()
        
        if msgType == self.__messenger.msgType:
            self.__messenger.handle(msgType, di)
            return
        
        AstronInternalRepository.handleDatagram(self, di)

    def getAvatarIdFromSender(self):
        return int(self.getMsgSender() & 0xFFFFFFFF)

    def getAccountIdFromSender(self):
        return int((self.getMsgSender()>>32) & 0xFFFFFFFF)

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000 and zoneId != 1:
            return False

        return True

    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
            
        except SystemExit, KeyboardInterrupt:
            raise
            
        except Exception as e:
            if self.getAvatarIdFromSender() > 100000000:
                dg = PyDatagram()
                dg.addServerHeader(self.getMsgSender(), self.ourChannel, CLIENTAGENT_EJECT)
                dg.addUint16(166)
                dg.addString('You were disconnected to prevent a district reset.')
                self.send(dg)
                
            self.writeServerEvent('INTERNAL-EXCEPTION', self.getAvatarIdFromSender(), self.getAccountIdFromSender(), repr(e), traceback.format_exc())
            self.notify.warning('INTERNAL-EXCEPTION: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
            print traceback.format_exc()
            sys.exc_clear()
            
        return 1
