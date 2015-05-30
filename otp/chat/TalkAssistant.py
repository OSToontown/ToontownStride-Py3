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


ThoughtPrefix = '.'


class TalkAssistant(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TalkAssistant')

    def __init__(self):
        self.logWhispers = 1
        self.clearHistory()
        self.zeroTimeDay = time.time()
        self.zeroTimeGame = globalClock.getRealTime()
        self.floodThreshold = 10.0
        self.lastWhisperDoId = None
        self.lastWhisper = None
        self.SCDecoder = SCDecoders
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
            messenger.send('NewOpenMessage', [newMessage])
        return error
