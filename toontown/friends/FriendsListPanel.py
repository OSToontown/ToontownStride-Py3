from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from toontown.toon import ToonAvatarPanel
from toontown.friends import ToontownFriendSecret
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPGlobals
FLPPets = 1
FLPOnline = 2
FLPAll = 3
globalFriendsList = None

def determineFriendName(friendTuple):
    if len(friendTuple) < 0:
        return None
    
    handle = base.cr.identifyFriend(friendTuple[0])
    return handle.getName() if handle else None


def compareFriends(f1, f2):
    name1 = determineFriendName(f1)
    name2 = determineFriendName(f2)
    if name1 > name2:
        return 1
    elif name1 == name2:
        return 0
    else:
        return -1


def showFriendsList():
    global globalFriendsList
    if globalFriendsList == None:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()
    return


def hideFriendsList():
    if globalFriendsList != None:
        globalFriendsList.exit()
    return


def showFriendsListTutorial():
    global globalFriendsList
    if globalFriendsList == None:
        globalFriendsList = FriendsListPanel()
    globalFriendsList.enter()
    globalFriendsList.closeCommand = globalFriendsList.close['command']
    globalFriendsList.close['command'] = None
    return


def hideFriendsListTutorial():
    if globalFriendsList != None:
        if hasattr(globalFriendsList, 'closeCommand'):
            globalFriendsList.close['command'] = globalFriendsList.closeCommand
        globalFriendsList.exit()
    return


def isFriendsListShown():
    if globalFriendsList != None:
        return globalFriendsList.isEntered
    return 0


def unloadFriendsList():
    global globalFriendsList
    if globalFriendsList != None:
        globalFriendsList.unload()
        globalFriendsList = None
    return


class FriendsListPanel(DirectFrame, StateData.StateData):

    def __init__(self):
        self.leftmostPanel = FLPPets
        self.rightmostPanel = FLPAll
        DirectFrame.__init__(self, relief=None)
        self.listScrollIndex = [0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0]
        self.initialiseoptions(FriendsListPanel)
        StateData.StateData.__init__(self, 'friends-list-done')
        self.friends = {}
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.panelType = FLPOnline
        return

    def load(self):
        if self.isLoaded == 1:
            return None
        self.isLoaded = 1
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        auxGui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.title = DirectLabel(parent=self, relief=None, text='', text_scale=TTLocalizer.FLPtitle, text_fg=(0, 0.1, 0.4, 1), pos=(0.007, 0.0, 0.2))
        background_image = gui.find('**/FriendsBox_Open')
        self['image'] = background_image
        self.reparentTo(base.a2dTopRight)
        self.setPos(-0.233, 0, -0.46)
        self.scrollList = DirectScrolledList(parent=self, relief=None, incButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_pos=(0.0, 0.0, -0.316), incButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), incButton_scale=(1.0, 1.0, -1.0), decButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_pos=(0.0, 0.0, 0.117), decButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), itemFrame_pos=(-0.17, 0.0, 0.06), itemFrame_relief=None, numItemsVisible=8, items=[])
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.2, 0, 0)))
        clipNP = self.scrollList.attachNewNode(clipper)
        self.scrollList.setClipPlane(clipNP)
        self.close = DirectButton(parent=self, relief=None, image=(auxGui.find('**/CloseBtn_UP'), auxGui.find('**/CloseBtn_DN'), auxGui.find('**/CloseBtn_Rllvr')), pos=(0.01, 0, -0.38), command=self.__close)
        self.left = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(-0.15, 0.0, -0.38), scale=(-1.0, 1.0, 1.0), command=self.__left)
        self.right = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(0.17, 0, -0.38), command=self.__right)
        self.newFriend = DirectButton(parent=self, relief=None, pos=(-0.14, 0.0, 0.14), image=(auxGui.find('**/Frnds_Btn_UP'), auxGui.find('**/Frnds_Btn_DN'), auxGui.find('**/Frnds_Btn_RLVR')), text=('', TTLocalizer.FriendsListPanelNewFriend, TTLocalizer.FriendsListPanelNewFriend), text_scale=TTLocalizer.FLPnewFriend, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(0.1, -0.085), textMayChange=0, command=self.__newFriend)
        self.secrets = DirectButton(parent=self, relief=None, pos=TTLocalizer.FLPsecretsPos, image=(auxGui.find('**/ChtBx_ChtBtn_UP'), auxGui.find('**/ChtBx_ChtBtn_DN'), auxGui.find('**/ChtBx_ChtBtn_RLVR')), text=('',
         TTLocalizer.FriendsListPanelSecrets,
         TTLocalizer.FriendsListPanelSecrets,
         ''), text_scale=TTLocalizer.FLPsecrets, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(-0.04, -0.085), textMayChange=0, command=self.__secrets)
        gui.removeNode()
        auxGui.removeNode()
        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        del self.title
        del self.scrollList
        del self.close
        del self.left
        del self.right
        del self.friends
        DirectFrame.destroy(self)
        return None

    def makeFriendButton(self, friendTuple, colorChoice = None, bold = 0):
        avId, flags = friendTuple
        command = self.__choseFriend
        handle = base.cr.identifyFriend(avId)
        if handle:
            toonName = handle.getName()
        else:
            base.cr.fillUpFriendsMap()
            return
        fg = ToontownGlobals.ColorNoChat
        if flags & ToontownGlobals.FriendChat:
            fg = ToontownGlobals.ColorAvatar
        if colorChoice:
            fg = colorChoice
        fontChoice = ToontownGlobals.getToonFont()
        fontScale = 0.04
        bg = None
        if colorChoice and bold:
            fontScale = 0.04
            colorS = 0.7
            bg = (colorChoice[0] * colorS,
             colorChoice[1] * colorS,
             colorChoice[2] * colorS,
             colorChoice[3])
        db = DirectButton(relief=None, text=toonName, text_scale=fontScale, text_align=TextNode.ALeft, text_fg=fg, text_shadow=bg, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, text_font=fontChoice, textMayChange=0, command=command, extraArgs=[avId])
        return db

    def enter(self):
        if self.isEntered == 1:
            return None
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        base.localAvatar.obscureFriendsListButton(1)
        if ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel:
            ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel.cleanup()
            ToonAvatarPanel.ToonAvatarPanel.currentAvatarPanel = None
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()
        self.show()
        self.accept('friendOnline', self.__friendOnline)
        self.accept('friendOffline', self.__friendOffline)
        self.accept('friendsListChanged', self.__friendsListChanged)
        self.accept('friendsMapComplete', self.__friendsListChanged)
        return

    def exit(self):
        if self.isEntered == 0:
            return None
        self.isEntered = 0
        self.listScrollIndex[self.panelType] = self.scrollList.index
        self.hide()
        base.cr.cleanPetsFromFriendsMap()
        self.ignore('friendOnline')
        self.ignore('friendOffline')
        self.ignore('friendsListChanged')
        self.ignore('friendsMapComplete')
        base.localAvatar.obscureFriendsListButton(-1)
        messenger.send(self.doneEvent)
        return None

    def __close(self):
        messenger.send('wakeup')
        self.exit()

    def __left(self):
        messenger.send('wakeup')
        self.listScrollIndex[self.panelType] = self.scrollList.index
        if self.panelType > self.leftmostPanel:
            self.panelType -= 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __right(self):
        messenger.send('wakeup')
        self.listScrollIndex[self.panelType] = self.scrollList.index
        if self.panelType < self.rightmostPanel:
            self.panelType += 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __secrets(self):
        messenger.send('wakeup')
        ToontownFriendSecret.showFriendSecret()

    def __newFriend(self):
        messenger.send('wakeup')
        messenger.send('friendAvatar', [None, None, None])
        return

    def __choseFriend(self, friendId):
        messenger.send('wakeup')
        handle = base.cr.identifyFriend(friendId)
        if handle != None:
            messenger.send('clickedNametag', [handle])

    def __updateScrollList(self):
        newFriends = []
        petFriends = []
        freeChatOneRef = []
        speedChatOneRef = []
        freeChatDouble = []
        speedChatDouble = []
        offlineFriends = []
        if self.panelType == FLPAll:
            if True:
                for friendPair in base.localAvatar.friendsList:
                    if base.cr.isFriendOnline(friendPair[0]):
                        if friendPair[1] & ToontownGlobals.FriendChat:
                            freeChatOneRef.insert(0, (friendPair[0],
                             friendPair[1]))
                        else:
                            speedChatOneRef.insert(0, (friendPair[0],
                             friendPair[1]))
                    elif friendPair[1] & ToontownGlobals.FriendChat:
                        freeChatOneRef.insert(0, (friendPair[0],
                         friendPair[1]))
                    else:
                        speedChatOneRef.insert(0, (friendPair[0],
                         friendPair[1]))

        if self.panelType == FLPOnline:
            if True:
                for friendPair in base.localAvatar.friendsList:
                    if base.cr.isFriendOnline(friendPair[0]):
                        offlineFriends.append((friendPair[0],
                         friendPair[1]))

        if self.panelType == FLPPets:
            for objId, obj in base.cr.doId2do.items():
                from toontown.pets import DistributedPet
                if isinstance(obj, DistributedPet.DistributedPet):
                    friendPair = (objId, 0)
                    petFriends.append(friendPair)

        if self.panelType == FLPAll or self.panelType == FLPOnline:
            if base.wantPets and base.localAvatar.hasPet():
                petFriends.insert(0, (base.localAvatar.getPetId(), 0))
        for friendPair in self.friends.keys():
            friendButton = self.friends[friendPair]
            self.scrollList.removeItem(friendButton, refresh=0)
            friendButton.destroy()
            del self.friends[friendPair]

        newFriends.sort(compareFriends)
        petFriends.sort(compareFriends)
        freeChatOneRef.sort(compareFriends)
        speedChatOneRef.sort(compareFriends)
        freeChatDouble.sort(compareFriends)
        speedChatDouble.sort(compareFriends)
        offlineFriends.sort(compareFriends)
        for friendPair in newFriends:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        for friendPair in petFriends:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair, ToontownGlobals.ColorNoChat, 0)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        for friendPair in freeChatDouble:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair, ToontownGlobals.ColorFreeChat, 1)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        for friendPair in freeChatOneRef:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair, ToontownGlobals.ColorFreeChat, 0)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        for friendPair in speedChatDouble:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair, ToontownGlobals.ColorSpeedChat, 1)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        for friendPair in speedChatOneRef:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair, ToontownGlobals.ColorSpeedChat, 0)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        for friendPair in offlineFriends:
            if friendPair not in self.friends:
                friendButton = self.makeFriendButton(friendPair, ToontownGlobals.ColorNoChat, 0)
                if friendButton:
                    self.scrollList.addItem(friendButton, refresh=0)
                    self.friends[friendPair] = friendButton

        self.scrollList.index = self.listScrollIndex[self.panelType]
        self.scrollList.refresh()

    def __updateTitle(self):
        if self.panelType == FLPOnline:
            self.title['text'] = TTLocalizer.FriendsListPanelOnlineFriends
        elif self.panelType == FLPAll:
            self.title['text'] = TTLocalizer.FriendsListPanelAllFriends
        else:
            self.title['text'] = TTLocalizer.FriendsListPanelPets
        self.title.resetFrameSize()

    def __updateArrows(self):
        if self.panelType == self.leftmostPanel:
            self.left['state'] = 'inactive'
        else:
            self.left['state'] = 'normal'
        if self.panelType == self.rightmostPanel:
            self.right['state'] = 'inactive'
        else:
            self.right['state'] = 'normal'

    def __friendOnline(self, doId, commonChatFlags, whitelistChatFlags):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendOffline(self, doId):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendsListChanged(self, arg1 = None, arg2 = None):
        self.__updateScrollList()