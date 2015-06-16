from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from pandac.PandaModules import *
import sys
import time

from otp.chat.ChatGlobals import *
from otp.chat.TalkGlobals import *
from otp.chat.TalkHandle import TalkHandle
from otp.chat.TalkMessage import TalkMessage
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from toontown.chat.ChatGlobals import *
from toontown.chat.TTWhiteList import TTWhiteList


ThoughtPrefix = '.'


class TalkAssistant(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TalkAssistant')

    def __init__(self):
        self.logWhispers = 1
        self.whiteList = None
        self.clearHistory()
        self.zeroTimeDay = time.time()
        self.zeroTimeGame = globalClock.getRealTime()
        self.floodThreshold = 10.0
        self.useWhiteListFilter = base.config.GetBool('white-list-filter-openchat', 0)
        self.lastWhisperDoId = None
        self.lastWhisper = None
        self.SCDecoder = SCDecoders
        self.whiteList = TTWhiteList()
        return

    def clearHistory(self):
        self.historyComplete = []
        self.historyOpen = []
        self.historyUpdates = []
        self.historyByDoId = {}
        self.historyByDISLId = {}
        self.floodDataByDoId = {}
        self.spamDictByDoId = {}
        self.handleDict = {}
        self.messageCount = 0
        self.shownWhiteListWarning = 0

    def delete(self):
        self.ignoreAll()
        self.clearHistory()

    def start(self):
        pass

    def stop(self):
        pass

    def countMessage(self):
        self.messageCount += 1
        return self.messageCount - 1

    def getOpenText(self, numLines, startPoint = 0):
        return self.historyOpen[startPoint:startPoint + numLines]

    def getSizeOpenText(self):
        return len(self.historyOpen)

    def getCompleteText(self, numLines, startPoint = 0):
        return self.historyComplete[startPoint:startPoint + numLines]

    def getCompleteTextFromRecent(self, numLines, startPoint = 0):
        start = len(self.historyComplete) - startPoint
        if start < 0:
            start = 0
        backStart = max(start - numLines, 0)
        text = self.historyComplete[backStart:start]
        text.reverse()
        return text

    def getAllCompleteText(self):
        return self.historyComplete

    def getAllHistory(self):
        return self.historyComplete

    def getSizeCompleteText(self):
        return len(self.historyComplete)

    def getHandle(self, doId):
        return self.handleDict.get(doId)

    def doWhiteListWarning(self):
        pass

    def addToHistoryDoId(self, message, doId, scrubbed = 0):
        if message.getTalkType() == TALK_WHISPER and doId != localAvatar.doId:
            self.lastWhisperDoId = doId
            self.lastWhisper = self.lastWhisperDoId
        if doId not in self.historyByDoId:
            self.historyByDoId[doId] = []
        self.historyByDoId[doId].append(message)
        if not self.shownWhiteListWarning and scrubbed and doId == localAvatar.doId:
            self.doWhiteListWarning()
            self.shownWhiteListWarning = 1
        if doId not in self.floodDataByDoId:
            self.floodDataByDoId[doId] = [0.0, self.stampTime(), message]
        else:
            oldTime = self.floodDataByDoId[doId][1]
            newTime = self.stampTime()
            timeDiff = newTime - oldTime
            oldRating = self.floodDataByDoId[doId][0]
            contentMult = 1.0
            if len(message.getBody()) < 6:
                contentMult += 0.2 * float(6 - len(message.getBody()))
            if self.floodDataByDoId[doId][2].getBody() == message.getBody():
                contentMult += 1.0
            floodRating = max(0, 3.0 * contentMult + oldRating - timeDiff)
            self.floodDataByDoId[doId] = [floodRating, self.stampTime(), message]
            if floodRating > self.floodThreshold:
                if oldRating < self.floodThreshold:
                    self.floodDataByDoId[doId] = [floodRating + 3.0, self.stampTime(), message]
                    return 1
                else:
                    self.floodDataByDoId[doId] = [oldRating - timeDiff, self.stampTime(), message]
                    return 2
        return 0

    def addToHistoryDISLId(self, message, dISLId, scrubbed = 0):
        if dISLId not in self.historyByDISLId:
            self.historyByDISLId[dISLId] = []
        self.historyByDISLId[dISLId].append(message)

    def addHandle(self, doId, message):
        if doId == localAvatar.doId:
            return
        handle = self.handleDict.get(doId)
        if not handle:
            handle = TalkHandle(doId, message)
            self.handleDict[doId] = handle
        else:
            handle.addMessageInfo(message)

    def stampTime(self):
        return globalClock.getRealTime() - self.zeroTimeGame

    def findAvatarName(self, id):
        info = base.cr.identifyAvatar(id)

        return info.getName() if info else ''

    def whiteListFilterMessage(self, text):
        if not self.useWhiteListFilter:
            return text
        elif not base.whiteList:
            return 'no list'
        words = text.split(' ')
        newwords = []
        for word in words:
            if word == '' or base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append(base.whiteList.defaultWord)

        newText = ' '.join(newwords)
        return newText

    def colorMessageByWhiteListFilter(self, text):
        if not base.whiteList:
            return text
        words = text.split(' ')
        newwords = []
        for word in words:
            if word == '' or base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append('\x01WLRed\x01' + word + '\x02')

        newText = ' '.join(newwords)
        return newText

    def isThought(self, message):
        if not message:
            return 0
        elif len(message) == 0:
            return 0
        elif message.find(ThoughtPrefix, 0, len(ThoughtPrefix)) >= 0:
            return 1
        else:
            return 0

    def removeThoughtPrefix(self, message):
        if self.isThought(message):
            return message[len(ThoughtPrefix):]
        else:
            return message

    def printHistoryComplete(self):
        print 'HISTORY COMPLETE'
        for message in self.historyComplete:
            print '%s %s %s\n%s\n' % (message.getTimeStamp(),
             message.getSenderAvatarName(),
             message.getSenderAccountName(),
             message.getBody())

    def checkOpenTypedChat(self):
        if base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
            return True
        return False

    def checkAnyTypedChat(self):
        if base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
            return True
        if base.localAvatar.canChat():
            return True
        return False

    def checkOpenSpeedChat(self):
        return True

    def checkWhisperTypedChatAvatar(self, avatarId):
        remoteAvatar = base.cr.doId2do.get(avatarId)
        if remoteAvatar:
            if remoteAvatar.isUnderstandable():
                return True
        if base.localAvatar.commonChatFlags & OTPGlobals.SuperChat:
            return True
        remoteAvatarOrHandleOrInfo = base.cr.identifyAvatar(avatarId)
        if remoteAvatarOrHandleOrInfo and hasattr(remoteAvatarOrHandleOrInfo, 'isUnderstandable'):
            if remoteAvatarOrHandleOrInfo.isUnderstandable():
                return True
        if base.cr.getFriendFlags(avatarId) & OTPGlobals.FriendChat:
            return True
        return False

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def checkOpenSpeedChat(self):
        return True

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def receiveOpenTalk(self, senderAvId, avatarName, accountId, accountName, message, scrubbed = 0):
        error = None
        if not avatarName and senderAvId:
            localAvatar.sendUpdate('logSuspiciousEvent', ['receiveOpenTalk: invalid avatar name (%s)' % senderAvId])
            avatarName = self.findAvatarName(senderAvId)
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, avatarName, accountId, accountName, None, None, None, None, TALK_OPEN, None)
        if senderAvId != localAvatar.doId:
            self.addHandle(senderAvId, newMessage)
        reject = 0
        if senderAvId:
            reject = self.addToHistoryDoId(newMessage, senderAvId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        if reject == 1:
            newMessage.setBody(OTPLocalizer.AntiSpamInChat)
        if reject != 2:
            isSpam = self.spamDictByDoId.get(senderAvId) and reject
            if not isSpam:
                self.historyComplete.append(newMessage)
                self.historyOpen.append(newMessage)
                messenger.send('NewOpenMessage', [newMessage])
            if newMessage.getBody() == OTPLocalizer.AntiSpamInChat:
                self.spamDictByDoId[senderAvId] = 1
            else:
                self.spamDictByDoId[senderAvId] = 0
        return error

    def receiveWhisperTalk(self, avatarId, avatarName, accountId, accountName, toId, toName, message, scrubbed = 0):
        error = None
        if not avatarName and avatarId:
            avatarName = self.findAvatarName(avatarId)
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, avatarId, avatarName, accountId, accountName, toId, toName, None, None, TALK_WHISPER, None)
        if avatarId == localAvatar.doId:
            self.addHandle(toId, newMessage)
        else:
            self.addHandle(avatarId, newMessage)
        self.historyComplete.append(newMessage)
        if avatarId:
            self.addToHistoryDoId(newMessage, avatarId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        messenger.send('NewOpenMessage', [newMessage])
        return error

    def receiveThought(self, avatarId, avatarName, accountId, accountName, message, scrubbed = 0):
        error = None
        if not avatarName and avatarId:
            avatarName = self.findAvatarName(avatarId)
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, avatarId, avatarName, accountId, accountName, None, None, None, None, AVATAR_THOUGHT, None)
        if avatarId != localAvatar.doId:
            self.addHandle(avatarId, newMessage)
        reject = 0
        if avatarId:
            reject = self.addToHistoryDoId(newMessage, avatarId, scrubbed)
        if accountId:
            self.addToHistoryDISLId(newMessage, accountId)
        if reject == 1:
            newMessage.setBody(OTPLocalizer.AntiSpamInChat)
        if reject != 2:
            self.historyComplete.append(newMessage)
            self.historyOpen.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])
        return error

    def receiveGameMessage(self, message):
        error = None
        if not self.isThought(message):
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, None, None, None, None, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, INFO_GAME, None)
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
        messenger.send('NewOpenMessage', [newMessage])
        return error

    def receiveSystemMessage(self, message):
        error = None
        if not self.isThought(message):
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, None, None, None, None, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, INFO_SYSTEM, None)
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
        messenger.send('NewOpenMessage', [newMessage])
        return error

    def receiveFriendUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline
        else:
            onlineMessage = OTPLocalizer.FriendOffline
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), onlineMessage, friendId, friendName, None, None, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, UPDATE_FRIEND, None)
        self.addHandle(friendId, newMessage)
        self.historyComplete.append(newMessage)
        self.historyUpdates.append(newMessage)
        messenger.send('NewOpenMessage', [newMessage])
        return

    def receiveFriendAccountUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline
        else:
            onlineMessage = OTPLocalizer.FriendOffline
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), onlineMessage, None, None, friendId, friendName, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, UPDATE_FRIEND, None)
        self.historyComplete.append(newMessage)
        self.historyUpdates.append(newMessage)
        messenger.send('NewOpenMessage', [newMessage])
        return

    def receiveOpenSpeedChat(self, type, messageIndex, senderAvId, name = None):
        error = None
        if not name and senderAvId:
            name = self.findAvatarName(senderAvId)
        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
        if message in (None, ''):
            return
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, name, None, None, None, None, None, None, TALK_OPEN, None)
        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        self.addToHistoryDoId(newMessage, senderAvId)
        messenger.send('NewOpenMessage', [newMessage])
        return error

    def receiveAvatarWhisperSpeedChat(self, type, messageIndex, senderAvId, name = None):
        error = None
        if not name and senderAvId:
            name = self.findAvatarName(senderAvId)
        if type == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
        elif type == SPEEDCHAT_CUSTOM:
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, name, None, None, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, TALK_WHISPER, None)
        self.historyComplete.append(newMessage)
        self.historyOpen.append(newMessage)
        self.addToHistoryDoId(newMessage, senderAvId)
        messenger.send('NewOpenMessage', [newMessage])
        return error

    def sendOpenTalk(self, message):
        error = None
        doId = base.localAvatar.doId
        if base.config.GetBool('want-talkative-tyler', False):
            if base.localAvatar.zoneId == 2000:
                tyler = base.cr.doFind('Talkative Tyler')
                if tyler:
                    tyler.sendUpdate('talkMessage', [doId, message])
        if base.cr.wantMagicWords and len(message) > 0 and message[0] == '~':
            messenger.send('magicWord', [message])
        else:
            chatFlags = CFSpeech | CFTimeout
            if self.isThought(message):
                chatFlags = CFThought
            base.cr.chatAgent.sendChatMessage(message)
            messenger.send('chatUpdate', [message, chatFlags])
        return error

    def sendWhisperTalk(self, message, receiverAvId):
        modifications = []
        words = message.split(' ')
        offset = 0
        WantWhitelist = config.GetBool('want-whitelist', 1)
        for word in words:
            if word and not self.whiteList.isWord(word) and WantWhitelist:
                modifications.append((offset, offset+len(word)-1))
            offset += len(word) + 1

        cleanMessage = message
        for modStart, modStop in modifications:
            cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

        message, scrubbed = base.localAvatar.scrubTalk(cleanMessage, modifications)

        base.cr.ttsFriendsManager.sendUpdate('sendTalkWhisper', [receiverAvId, message])

    def sendOpenSpeedChat(self, type, messageIndex):
        error = None
        if type == SPEEDCHAT_NORMAL:
            messenger.send(SCChatEvent)
            messenger.send('chatUpdateSC', [messageIndex])
            base.localAvatar.b_setSC(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            messenger.send('chatUpdateSCEmote', [messageIndex])
            messenger.send(SCEmoteChatEvent)
            base.localAvatar.b_setSCEmote(messageIndex)
        elif type == SPEEDCHAT_CUSTOM:
            messenger.send('chatUpdateSCCustom', [messageIndex])
            messenger.send(SCCustomChatEvent)
            base.localAvatar.b_setSCCustom(messageIndex)
        return error

    def sendAvatarWhisperSpeedChat(self, type, messageIndex, receiverId):
        error = None
        if type == SPEEDCHAT_NORMAL:
            base.localAvatar.whisperSCTo(messageIndex, receiverId)
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            base.localAvatar.whisperSCEmoteTo(messageIndex, receiverId)
            message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, localAvatar.getName())
        elif type == SPEEDCHAT_CUSTOM:
            base.localAvatar.whisperSCCustomTo(messageIndex, receiverId)
            message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
        if self.logWhispers:
            avatarName = None
            accountId = None
            avatar = base.cr.identifyAvatar(receiverId)
            if avatar:
                avatarName = avatar.getName()
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, receiverId, avatarName, None, None, TALK_WHISPER, None)
            self.historyComplete.append(newMessage)
            self.addToHistoryDoId(newMessage, localAvatar.doId)
            messenger.send('NewOpenMessage', [newMessage])
        return error
