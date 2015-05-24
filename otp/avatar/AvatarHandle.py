class AvatarHandle:
    dclassName = 'AvatarHandle'

    def getName(self):
        return ''

    def isOnline(self):
        return False

    def isUnderstandable(self):
        return True

    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        if not base.cr.chatAgent.verifyMessage(chat):
            return
        newText, scrubbed = localAvatar.scrubTalk(chat, mods)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.avatarId, self.getName(), newText, scrubbed)