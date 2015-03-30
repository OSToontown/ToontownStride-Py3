from pandac.PandaModules import *
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToontownBattleGlobals import AvPropsNew

class TrackShop(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('TrackShop')

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.quest = None
        self.label = None
        self.leftButton = None
        self.rightButton = None
        self.track = None
        self.icon = None
        self.loaded = False
        self.index = 0
        return

    def enter(self):
        base.disableMouse()
        self.acceptOnce('last', self.__handleBackward)
        self.acceptOnce('next', self.__handleForward)

    def showButtons(self):
        for element in [self.quest, self.label, self.leftButton, self.rightButton, self.track, self.icon]:
            element.show()

    def hideButtons(self):
        for element in [self.quest, self.label, self.leftButton, self.rightButton, self.track, self.icon]:
            element.hide()

    def exit(self):
        self.ignore('last')
        self.ignore('next')
        self.hideButtons()

    def load(self):
        if self.loaded:
            return
        
        self.loaded = True
        self.questGui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        self.inventoryGui = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        self.buttonGui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        self.shuffleArrowUp = self.buttonGui.find('**/tt_t_gui_mat_shuffleArrowUp')
        self.shuffleArrowDown = self.buttonGui.find('**/tt_t_gui_mat_shuffleArrowDown')

        self.quest = DirectFrame(aspect2d, relief=None, image=self.questGui.find('**/questCard'),
                     pos=(-0.62, 0, 0), image_scale=1.5)

        self.label = DirectLabel(aspect2d, relief=None, text=TTLocalizer.PickTrackNotice,
                     text_fg=(0, 1, 0, 1), text_scale=0.12, text_font=ToontownGlobals.getToonFont(),
                     pos=(-0.62, 0, 0.45), text_shadow=(0, 0.392, 0, 1))
        
        self.leftButton = DirectButton(aspect2d, relief=None, image=(self.shuffleArrowUp, self.shuffleArrowDown),
                          pos=(-1.2, 0, -0.05), command=self.handleSetIndex, extraArgs=[-1])

        self.rightButton = DirectButton(aspect2d, relief=None, image=(self.shuffleArrowUp, self.shuffleArrowDown),
                           pos=(-0.05, 0, -0.05), scale=-1, command=self.handleSetIndex, extraArgs=[1])
        
        self.track = DirectLabel(aspect2d, relief=None, text='',
                     text_scale=0.11, text_font=ToontownGlobals.getSignFont(),
                     pos=(-0.64, 0, -0.08), text_shadow=(1, 1, 1, 1))
        
        self.icon = DirectFrame(aspect2d, relief=None, pos=(-0.65, 0, -0.3), image_scale=1.5)
        
        self.updateGuiByIndex()

    def unload(self):
        for element in [self.quest, self.label, self.leftButton, self.rightButton, self.track, self.icon]:
            if element:
                element.destroy()
                del element
        
        self.index = 0
        self.loaded = False
    
    def handleSetIndex(self, offset):
        newIndex = self.index + offset
        
        if newIndex == 4:
            self.index = 6
        elif newIndex == 5:
            self.index = 3
        elif newIndex > -1 and newIndex < len(ToontownGlobals.PropIdToColor):
            self.index = newIndex
         
        self.updateGuiByIndex()
    
    def updateGuiByIndex(self):
        self.track['text'] = TTLocalizer.PropIdToName[self.index]
        self.track['text_fg'] = ToontownGlobals.PropIdToColor[self.index]
        self.icon['image'] = self.inventoryGui.find('**/' + AvPropsNew[self.index][0])
    
    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)
