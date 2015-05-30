from otp.avatar.AvatarHandle import AvatarHandle

class TalkHandle(AvatarHandle):

    def __init__(self, doId, message):
        self.avatarId = doId
        self.avatarName = None
        self.accountId = None
        self.accountName = None
        self.addMessageInfo(message)
        return

    def getName(self):
        return self.avatarName

    def isUnderstandable(self):
        return False

    def isOnline(self):
        return False

    def addMessageInfo(self, message):
        if self.avatarId == message.getSenderAvatarId():
            if not self.avatarName and message.getSenderAvatarName():
                self.avatarName = message.getSenderAvatarName()
            if not self.accountId and message.getSenderAccountId():
                self.accountId = message.getSenderAccountId()
            if not self.accountName and message.getSenderAccountName():
                self.accountName = message.getSenderAccountName()
        elif self.avatarId == message.getReceiverAvatarId():
            if not self.avatarName and message.getReceiverAvatarName():
                self.avatarName = message.getReceiverAvatarName()
            if not self.accountId and message.getReceiverAccountId():
                self.accountId = message.getReceiverAccountId()
            if not self.accountName and message.getReceiverAccountName():
                self.accountName = message.getReceiverAccountName()