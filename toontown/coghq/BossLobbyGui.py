from pandac.PandaModules import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class BossLobbyGui(DirectFrame):

    class InitialFrame(DirectFrame):

        frame = 0

        class LobbySelection(DirectButton):

            def __init__(self, parent, **kw):
                optiondefs = (
                    ('relief', None, None),
                    ('image_scale', 0.55, None),
                    ('text_pos', (0.3, -0.0225), None),
                    ('text_scale', 0.075, None),
                )
                self.defineoptions(kw, optiondefs)
                DirectButton.__init__(self, relief=None)
                self.initialiseoptions(BossLobbyGui.InitialFrame.LobbySelection)

        def __init__(self, parent, callback, **kw):
            optiondefs = (
                ('relief', None, None),
                ('state', DGG.NORMAL, None),
                ('image', DGG.getDefaultDialogGeom(), None),
                ('image_scale', (1.0, 1.0, 0.75), None),
                ('image_color', ToontownGlobals.GlobalDialogColor, None),
                ('pos', (0, 0, 0), None),
            )
            self.defineoptions(kw, optiondefs)
            DirectFrame.__init__(self, relief=None)
            self.initialiseoptions(BossLobbyGui.InitialFrame)
            self.callback = callback
            self.load()
            self.selection = -1

        def destroy(self):
            self.title.destroy()
            for button in self.buttons:
                button.destroy()
            self.okButton.destroy()
            self.cancelButton.destroy()
            DirectFrame.destroy(self)

        def load(self):
            empty = loader.loadModel("phase_3.5/models/gui/matching_game_gui.bam")
            check = loader.loadModel("phase_3.5/models/gui/name_star")
            buttons = loader.loadModel("phase_3/models/gui/dialog_box_buttons_gui")
            self.emptyList = (empty.find("**/minnieCircle"), empty.find("**/minnieCircle"), empty.find("**/minnieCircle"))
            self.checkList = (check.find("**/*"), check.find("**/*"), check.find("**/*"))
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            empty.removeNode()
            check.removeNode()
            buttons.removeNode()
            self.title = DirectLabel(parent=self, relief=None, text="Select a Lobby", textMayChange=1, text_scale=0.1, pos=(0, 0, 0.25))
            self.okButton = DirectButton(parent=self, relief=None, image=okImageList, pos=(-0.1, 0, -0.275), command=self.nextFrame, extraArgs=[True])
            self.cancelButton = DirectButton(parent=self, relief=None, image=cancelImageList, pos=(0.1, 0, -0.275), command=self.nextFrame, extraArgs=[False])
            self.buttons = []
            public = BossLobbyGui.InitialFrame.LobbySelection(self, image=self.emptyList, pos=(-0.35, 0, 0.075), text="Public", command=self.setSelection, extraArgs=[0])
            private = BossLobbyGui.InitialFrame.LobbySelection(self, image=self.emptyList, pos=(-0.3475, 0, -0.075), text="Private", command=self.setSelection, extraArgs=[1])
            self.buttons.extend([
                public,
                private
            ])

        def unload(self):
            self.title.destroy()
            self.public.destroy()
            self.private.destroy()
            self.okButton.destroy()
            self.cancelButton.destroy()
            del self.title
            del self.public
            del self.private
            del self.okButton
            del self.cancelButton

        def setSelection(self, buttonId):
            newSelection = self.buttons[buttonId]
            if newSelection:
                for button in self.buttons:
                    button['image'] = self.emptyList
                    button['image_scale'] = 0.55
                    button.setColor(1, 1, 1, 1)
                newSelection['image'] = self.checkList
                newSelection['image_scale'] = 0.11
                newSelection.setColor(0, 1, 0, 1)
            self.selection = buttonId

        def getSelection(self):
            return self.selection

        def nextFrame(self, status):
            if status and self.getSelection() >= 0:
                options = {
                    'lobbyType': self.getSelection()
                }
                self.callback(self.frame + 1, options)
            else:
                self.callback(-1)

    def __init__(self, callback, av):
        DirectFrame.__init__(self)
        self.callback = callback
        self.avatar = av
        self.frame = None
        self.loadFrame(0)

    def destroy(self):
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
        DirectFrame.destroy(self)

    def loadFrame(self, frameNum, args={}):
        if hasattr(self, 'frame') and self.frame:
            self.frame.destroy()
        if frameNum == -1:
            self.callback(self.avatar, False)
        elif frameNum == 0:
            self.frame = BossLobbyGui.InitialFrame(self, self.loadFrame)
        elif frameNum == 1 and args.get('lobbyType') is not None:
            lobby = args.get('lobbyType')
            if lobby == 0:
                self.callback(self.avatar, True)
            elif lobby == 1:
                self.callback(self.avatar, True)

# Use the following to run with the Gui Editor.
"""
from pandac.PandaModules import *
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from toontown.coghq.BossLobbyGui import BossLobbyGui
from toontown.toonbase import ToontownGlobals

DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))

test = BossLobbyGui(None, None)
"""
