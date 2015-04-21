from pandac.PandaModules import *
from panda3d.core import NodePath, ModelNode
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownBattleGlobals

class TrackShop(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('TrackShop')

    def __init__(self, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.loaded = False
        self.index = 0
        self.buttonPath = None
        self.curTrackLabel = None
        return

    def showButtons(self):
        self.buttonPath.show()
        self.curTrackLabel.show()

    def hideButtons(self):
        self.buttonPath.hide()
        self.curTrackLabel.hide()

    def enter(self):
        base.disableMouse()
        self.acceptOnce('last', self.__handleBackward)
        self.acceptOnce('next', self.__handleForward)

    def exit(self):
        self.ignore('last')
        self.ignore('next')
        self.hideButtons()

    def load(self):
        if self.loaded:
            return
        self.loaded = True

        buttonModel = ModelNode('tracks')
        self.buttonPath = NodePath(buttonModel)

        self.curTrackLabel = DirectLabel(aspect2d, relief=None,
                                         text='toon-up', text_scale=0.12, text_font=ToontownGlobals.getSignFont(), text_fg=(1, 0, 0, 1),
                                         pos=(0, 0, -0.9))

        buttonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")

        availableTracks = [(0, 'toon-up'), (1, 'trap'), (2, 'lure'), (3, 'sound'), (4, 'drop')]
        for i, track in reversed(availableTracks):
            track = DirectButton(self.buttonPath, relief=None,
                                 text=track, text_scale=0.08, text_font=ToontownGlobals.getSignFont(), text_pos=(0, -0.03), text_fg=(1, 0, 0, 1),
                                 pos=(0, 0, (i * 0.15) - 0.5),
                                 image=(buttonImage.find('**/QuitBtn_UP'), buttonImage.find('**/QuitBtn_DN'), buttonImage.find('**/QuitBtn_RLVR')),
                                 command=self.handleSetIndex, extraArgs=[i, track])

        self.buttonPath.reparentTo(aspect2d)

    def unload(self):
        if self.buttonPath:
            self.buttonPath.removeNode()
            del self.buttonPath
        if self.curTrackLabel:
            self.curTrackLabel.removeNode()
            del self.curTrackLabel
        self.index = 0
        self.loaded = False
    
    def handleSetIndex(self, i, track):
        self.index = i
        self.curTrackLabel['text'] = track
    
    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)
