from otp.avatar.Avatar import teleportNotify
from toontown.toonbase import ToontownGlobals
import copy
from toontown.chat import ToonChatGarbler


class FriendHandle:
    def __init__(self, doId, name, style, petId, isAPet = False):
        self.doId = doId
        self.style = style
        self.petId = petId
        self.isAPet = isAPet
        self.chatGarbler = ToonChatGarbler.ToonChatGarbler()
        self.name = name

    def getDoId(self):
        return self.doId

    def getPetId(self):
        return self.petId

    def hasPet(self):
        return self.getPetId() != 0

    def isPet(self):
        return self.isAPet

    def getName(self):
        return self.name

    def getFont(self):
        return ToontownGlobals.getToonFont()

    def getStyle(self):
        return self.style

    def uniqueName(self, idString):
        return idString + '-' + str(self.getDoId())

    def d_battleSOS(self, sendToId):
        base.cr.ttsFriendsManager.d_battleSOS(self.doId)

    def d_teleportQuery(self, requesterId):
        teleportNotify.debug('sending d_teleportQuery(%s)' % (requesterId,))

        base.cr.ttsFriendsManager.d_teleportQuery(self.doId)

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        teleportNotify.debug('sending teleportResponse%s' % ((avId, available,
            shardId, hoodId, zoneId),)
        )

        base.cr.ttsFriendsManager.d_teleportResponse(self.doId, available,
            shardId, hoodId, zoneId
        )

    def d_teleportGiveup(self, requesterId):
        teleportNotify.debug('sending d_teleportGiveup(%s)' % (requesterId,))

        base.cr.ttsFriendsManager.d_teleportGiveup(self.doId)

    def isUnderstandable(self):
        if settings['speedchatPlus']:
            return 1
        elif settings['trueFriends'] and base.cr.getFriendFlags(self.doId) & ToontownGlobals.FriendChat:
            return 1
        return 0

    def scrubTalk(self, message, mods):
        scrubbed = 0
        text = copy.copy(message)
        for mod in mods:
            index = mod[0]
            length = mod[1] - mod[0] + 1
            newText = text[0:index] + length * '\x07' + text[index + length:]
            text = newText

        words = text.split(' ')
        newwords = []
        for word in words:
            if word == '':
                newwords.append(word)
            elif word[0] == '\x07':
                newwords.append('\x01WLDisplay\x01' + self.chatGarbler.garbleSingle(self, word) + '\x02')
                scrubbed = 1
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append('\x01WLDisplay\x01' + word + '\x02')
                scrubbed = 1

        newText = ' '.join(newwords)
        return (newText, scrubbed)

    def replaceBadWords(self, text):
        words = text.split(' ')
        newwords = []
        for word in words:
            if word == '':
                newwords.append(word)
            elif word[0] == '\x07':
                newwords.append('\x01WLRed\x01' + self.chatGarbler.garbleSingle(self, word) + '\x02')
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append('\x01WLRed\x01' + word + '\x02')

        newText = ' '.join(newwords)
        return newText
