from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.chat import ChatManager
from TTChatInputSpeedChat import TTChatInputSpeedChat
from TTChatInputWhiteList import TTChatInputWhiteList

class ToontownChatManager(ChatManager.ChatManager):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownChatManager')

    def __init__(self, cr, localAvatar):
        gui = loader.loadModel('phase_3.5/models/gui/chat_input_gui')
        self.normalButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(0.0683, 0, -0.072), parent=base.a2dTopLeft, scale=1.179, relief=None, image_color=Vec4(1, 1, 1, 1), text=('', OTPLocalizer.ChatManagerChat, OTPLocalizer.ChatManagerChat), text_align=TextNode.ALeft, text_scale=TTLocalizer.TCMnormalButton, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(-0.0525, -0.09), textMayChange=0, sortOrder=DGG.FOREGROUND_SORT_INDEX, command=self.__normalButtonPressed)
        self.normalButton.hide()
        self.openScSfx = loader.loadSfx('phase_3.5/audio/sfx/GUI_quicktalker.ogg')
        self.openScSfx.setVolume(0.6)
        self.scButton = DirectButton(image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=TTLocalizer.TCMscButtonPos, parent=base.a2dTopLeft, scale=1.179, relief=None, image_color=Vec4(0.75, 1, 0.6, 1), text=('', OTPLocalizer.GlobalSpeedChatName, OTPLocalizer.GlobalSpeedChatName), text_scale=TTLocalizer.TCMscButton, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, sortOrder=DGG.FOREGROUND_SORT_INDEX, command=self.__scButtonPressed, clickSound=self.openScSfx)
        self.scButton.hide()
        self.whisperFrame = DirectFrame(parent=base.a2dTopLeft, relief=None, image=DGG.getDefaultDialogGeom(), image_scale=(0.45, 0.45, 0.45), image_color=OTPGlobals.GlobalDialogColor, pos=(1.25, 0, -0.269), text=OTPLocalizer.ChatManagerWhisperTo, text_wordwrap=7.0, text_scale=TTLocalizer.TCMwhisperFrame, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0.14), textMayChange=1, sortOrder=DGG.FOREGROUND_SORT_INDEX)
        self.whisperFrame.hide()
        self.whisperButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(-0.125, 0, -0.1), scale=1.179, relief=None, image_color=Vec4(1, 1, 1, 1), text=('',
         OTPLocalizer.ChatManagerChat,
         OTPLocalizer.ChatManagerChat,
         ''), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), text_scale=TTLocalizer.TCMwhisperButton, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, command=self.__whisperButtonPressed)
        self.whisperScButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/ChtBx_ChtBtn_UP'), gui.find('**/ChtBx_ChtBtn_DN'), gui.find('**/ChtBx_ChtBtn_RLVR')), pos=(0.0, 0, -0.1), scale=1.179, relief=None, image_color=Vec4(0.75, 1, 0.6, 1), text=('',
         OTPLocalizer.GlobalSpeedChatName,
         OTPLocalizer.GlobalSpeedChatName,
         ''), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), text_scale=TTLocalizer.TCMwhisperScButton, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, command=self.__whisperScButtonPressed)
        self.whisperCancelButton = DirectButton(parent=self.whisperFrame, image=(gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'), gui.find('**/CloseBtn_Rllvr')), pos=(0.125, 0, -0.1), scale=1.179, relief=None, text=('', OTPLocalizer.ChatManagerCancel, OTPLocalizer.ChatManagerCancel), text_scale=0.05, text_fg=(0, 0, 0, 1), text_pos=(0, -0.09), textMayChange=0, command=self.__whisperCancelPressed)
        gui.removeNode()
        ChatManager.ChatManager.__init__(self, cr, localAvatar)
        self.chatInputSpeedChat = TTChatInputSpeedChat(self)
        self.normalPos = Vec3(0.25, 0, -0.196)
        self.whisperPos = Vec3(0, 0, -0.296)
        self.speedChatPlusPos = Vec3(-0.35, 0, 0.71)
        self.SCWhisperPos = Vec3(0, 0, 0)
        self.chatInputWhiteList = TTChatInputWhiteList()
        self.chatInputNormal = self.chatInputWhiteList
        self.chatInputNormal.setPos(self.normalPos)
        self.chatInputNormal.desc = 'chatInputNormal'
        self.chatInputWhiteList.setPos(self.speedChatPlusPos)
        self.chatInputWhiteList.reparentTo(base.a2dTopLeft)
        self.chatInputWhiteList.desc = 'chatInputWhiteList'
        return

    def delete(self):
        ChatManager.ChatManager.delete(self)
        loader.unloadModel('phase_3.5/models/gui/chat_input_gui')
        self.normalButton.destroy()
        del self.normalButton
        self.scButton.destroy()
        del self.scButton
        del self.openScSfx
        self.whisperFrame.destroy()
        del self.whisperFrame
        self.whisperButton.destroy()
        del self.whisperButton
        self.whisperScButton.destroy()
        del self.whisperScButton
        self.whisperCancelButton.destroy()
        del self.whisperCancelButton
        self.chatInputWhiteList.destroy()
        del self.chatInputWhiteList

    def sendSCResistanceChatMessage(self, textId):
        messenger.send('chatUpdateSCResistance', [textId])
        self.announceSCChat()

    def sendSCSingingChatMessage(self, textId):
        messenger.send('chatUpdateSCSinging', [textId])
        self.announceSCChat()

    def sendSCSingingWhisperMessage(self, textId):
        pass

    def sendSCToontaskChatMessage(self, taskId, toNpcId, toonProgress, msgIndex):
        messenger.send('chatUpdateSCToontask', [taskId,
         toNpcId,
         toonProgress,
         msgIndex])
        self.announceSCChat()

    def sendSCToontaskWhisperMessage(self, taskId, toNpcId, toonProgress, msgIndex, whisperAvatarId):
        messenger.send('whisperUpdateSCToontask', [taskId,
         toNpcId,
         toonProgress,
         msgIndex,
         whisperAvatarId])

    def enterMainMenu(self):
        self.chatInputNormal.setPos(self.normalPos)
        self.chatInputNormal.reparentTo(base.a2dTopLeft)
        if self.chatInputWhiteList.isActive():
            self.notify.debug('enterMainMenu calling checkObscured')
            ChatManager.ChatManager.checkObscurred(self)
        else:
            ChatManager.ChatManager.enterMainMenu(self)

    def enterNoSecretChatAtAll(self):
        if self.noSecretChatAtAll == None:
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.noSecretChatAtAll = DirectFrame(parent=aspect2dp, pos=(0.0, 0.1, 0.2), relief=None, image=DGG.getDefaultDialogGeom(), image_color=OTPGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.1), text=OTPLocalizer.NoSecretChatAtAll, text_wordwrap=20, textMayChange=0, text_scale=0.06, text_pos=(0, 0.3))
            DirectLabel(parent=self.noSecretChatAtAll, relief=None, pos=(0, 0, 0.4), text=OTPLocalizer.NoSecretChatAtAllTitle, textMayChange=0, text_scale=0.08)
            DirectButton(self.noSecretChatAtAll, image=okButtonImage, relief=None, text=OTPLocalizer.NoSecretChatAtAllOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.4), command=self.__handleNoSecretChatAtAllOK)
            buttons.removeNode()
        self.noSecretChatAtAll.show()
        return

    def exitNoSecretChatAtAll(self):
        self.noSecretChatAtAll.hide()

    def __normalButtonPressed(self):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: CHAT: Speedchat Plus')
        messenger.send('wakeup')
        self.fsm.request('normalChat')

    def __scButtonPressed(self):
        messenger.send('wakeup')
        if self.fsm.getCurrentState().getName() == 'speedChat':
            self.fsm.request('mainMenu')
        else:
            self.fsm.request('speedChat')

    def __whisperButtonPressed(self, avatarName, avatarId):
        messenger.send('wakeup')
        if avatarId:
            self.enterWhisperChat(avatarName, avatarId)
        self.whisperFrame.hide()
        return

    def enterNormalChat(self):
        result = ChatManager.ChatManager.enterNormalChat(self)
        if result == None:
            self.notify.warning('something went wrong in enterNormalChat, falling back to main menu')
            self.fsm.request('mainMenu')
        return

    def enterWhisperChat(self, avatarName, avatarId):
        result = ChatManager.ChatManager.enterWhisperChat(self, avatarName, avatarId)
        self.chatInputNormal.reparentTo(base.a2dTopCenter)
        self.chatInputNormal.setPos(self.whisperPos)
        if result == None:
            self.notify.warning('something went wrong in enterWhisperChat, falling back to main menu')
            self.fsm.request('mainMenu')
        return

    def enterNoSecretChatAtAllAndNoWhitelist(self):
        if self.noSecretChatAtAllAndNoWhitelist == None:
            buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            self.noSecretChatAtAllAndNoWhitelist = DirectFrame(parent=aspect2dp, pos=(0.0, 0.1, 0.05), relief=None, image=DGG.getDefaultDialogGeom(), image_color=OTPGlobals.GlobalDialogColor, image_scale=(1.4, 1.0, 1.58), text=OTPLocalizer.NoSecretChatAtAllAndNoWhitelist, text_wordwrap=20, textMayChange=0, text_scale=0.06, text_pos=(0, 0.55))
            DirectLabel(parent=self.noSecretChatAtAllAndNoWhitelist, relief=None, pos=(0, 0, 0.67), text=OTPLocalizer.NoSecretChatAtAllAndNoWhitelistTitle, textMayChange=0, text_scale=0.08)
            DirectButton(self.noSecretChatAtAllAndNoWhitelist, image=okButtonImage, relief=None, text=OTPLocalizer.NoSecretChatAtAllOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.64), command=self.__handleNoSecretChatAtAllOK)
            buttons.removeNode()
        self.noSecretChatAtAllAndNoWhitelist.show()
        return

    def exitNoSecretChatAtAllAndNoWhitelist(self):
        self.noSecretChatAtAllAndNoWhitelist.hide()

    def __whisperScButtonPressed(self, avatarName, avatarId):
        messenger.send('wakeup')
        if avatarId:
            if self.fsm.getCurrentState().getName() == 'whisperSpeedChat':
                self.fsm.request('whisper', [avatarName, avatarId])
            else:
                self.fsm.request('whisperSpeedChat', [avatarId])

    def __whisperCancelPressed(self):
        self.fsm.request('mainMenu')

    def __handleNoSecretChatAtAllOK(self):
        self.fsm.request('mainMenu')

    def messageSent(self):
        pass