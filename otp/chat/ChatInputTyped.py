from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from pandac.PandaModules import *
import sys

from otp.chat import ChatUtil
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from toontown.chat.ChatGlobals import *


class ChatInputTyped(DirectObject.DirectObject):
    def __init__(self, mainEntry = 0):
        self.whisperName = None
        self.whisperId = None
        self.mainEntry = mainEntry
        self.wantHistory = base.config.GetBool('want-chat-history', 0)
        self.history = ['']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0
        return

    def typeCallback(self, extraArgs):
        self.activate()

    def delete(self):
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')
        self.chatFrame.destroy()
        del self.chatFrame
        del self.chatButton
        del self.cancelButton
        del self.chatEntry
        del self.whisperLabel
        del self.chatMgr

    def show(self, whisperId = None):
        self.whisperId = whisperId
        self.whisperName = None
        if self.whisperId:
            self.whisperName = ChatUtil.findAvatarName(whisperId)
            if hasattr(self, 'whisperPos'):
                self.chatFrame.setPos(self.whisperPos)
            self.whisperLabel['text'] = OTPLocalizer.ChatInputWhisperLabel % self.whisperName
            self.whisperLabel.show()
        else:
            if hasattr(self, 'normalPos'):
                self.chatFrame.setPos(self.normalPos)
            self.whisperLabel.hide()
        self.chatEntry['focus'] = 1
        self.chatEntry.set('')
        self.chatFrame.show()
        self.chatEntry.show()
        self.cancelButton.show()
        self.typedChatButton.hide()
        self.typedChatBar.hide()
        if self.wantHistory:
            self.accept('arrow_up-up', self.getPrevHistory)
            self.accept('arrow_down-up', self.getNextHistory)
        return

    def hide(self):
        self.chatEntry.set('')
        self.chatEntry['focus'] = 0
        self.chatFrame.hide()
        self.chatEntry.hide()
        self.cancelButton.hide()
        self.typedChatButton.show()
        self.typedChatBar.show()
        self.ignore('arrow_up-up')
        self.ignore('arrow_down-up')

    def activate(self):
        self.chatEntry.set('')
        self.chatEntry['focus'] = 1
        self.chatFrame.show()
        self.chatEntry.show()
        self.cancelButton.show()
        self.typedChatButton.hide()
        self.typedChatBar.hide()

    def deactivate(self):
        self.chatEntry.set('')
        self.chatEntry['focus'] = 0
        self.chatFrame.show()
        self.chatEntry.hide()
        self.cancelButton.hide()
        self.typedChatButton.show()
        self.typedChatBar.show()

    def sendChat(self, text):
        self.deactivate()
        if text:
            if self.whisperId:
                pass
            else:
                base.talkAssistant.sendOpenTalk(text)
            if self.wantHistory:
                self.addToHistory(text)
        self.chatEntry.set('')

    def chatOverflow(self, overflowText):
        self.sendChat(self.chatEntry.get())

    def cancelButtonPressed(self):
        self.chatEntry.set('')
        self.deactivate()

    def chatButtonPressed(self):
        self.sendChat(self.chatEntry.get())

    def addToHistory(self, text):
        self.history = [text] + self.history[:self.historySize - 1]
        self.historyIndex = 0

    def getPrevHistory(self):
        self.chatEntry.set(self.history[self.historyIndex])
        self.historyIndex += 1
        self.historyIndex %= len(self.history)

    def getNextHistory(self):
        self.chatEntry.set(self.history[self.historyIndex])
        self.historyIndex -= 1
        self.historyIndex %= len(self.history)
