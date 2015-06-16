import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from pandac.PandaModules import *
from otp.chat.ChatGlobals import *
from otp.chat.TalkGlobals import *
from otp.speedchat import SpeedChatGlobals
from otp.chat.TalkMessage import TalkMessage
from otp.chat.TalkAssistant import TalkAssistant
from toontown.speedchat import TTSCDecoders
import time

class TTTalkAssistant(TalkAssistant):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTTalkAssistant')

    def __init__(self):
        TalkAssistant.__init__(self)

    def clearHistory(self):
        TalkAssistant.clearHistory(self)

    def sendToonTaskSpeedChat(self, taskId, toNpcId, toonProgress, msgIndex):
        error = None
        messenger.send(SCChatEvent)
        messenger.send('chatUpdateSCToontask', [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
        return error
