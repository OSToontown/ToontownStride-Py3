from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownNetMessengerAI import ToontownNetMessengerAI

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
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender()>>32) & 0xFFFFFFFF

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000 and zoneId != 1:
            return False

        return True
