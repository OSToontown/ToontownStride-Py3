from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from otp.distributed import OtpDoGlobals

class ChatAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("ChatAgentUD")

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.chatMode2channel = {
            1 : OtpDoGlobals.OTP_MOD_CHANNEL,
            2 : OtpDoGlobals.OTP_ADMIN_CHANNEL,
            3 : OtpDoGlobals.OTP_SYSADMIN_CHANNEL,
        }
        self.chatMode2prefix = {
            1 : "[MOD] ",
            2 : "[ADMIN] ",
            3 : "[SYSADMIN] ",
        }

    def chatMessage(self, message, chatMode):
        sender = self.air.getAvatarIdFromSender()

        if sender == 0:
            self.air.writeServerEvent('suspicious', accId=self.air.getAccountIdFromSender(),
                                      issue='Account sent chat without an avatar', message=message)
            return

        self.air.writeServerEvent('chat-said', avId=sender, chatMode=chatMode, msg=message)

        if chatMode != 0:
            if message.startswith('.'):
                message = '.' + self.chatMode2prefix.get(chatMode, "") + message[1:]
            else:
                message = self.chatMode2prefix.get(chatMode, "") + message

        DistributedAvatar = self.air.dclassesByName['DistributedAvatarUD']
        dg = DistributedAvatar.aiFormatUpdate('setTalk', sender, self.chatMode2channel.get(chatMode, sender), self.air.ourChannel, [message])
        self.air.send(dg)
