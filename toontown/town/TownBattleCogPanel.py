from direct.gui.DirectGui import *
from toontown.suit import Suit, SuitHealthBar
from toontown.toonbase import TTLocalizer

class TownBattleCogPanel(DirectFrame):

    def __init__(self, id):
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=(0.86, 0.86, 0.86, 0.7), scale=0.8)
        self.initialiseoptions(TownBattleCogPanel)
        self.levelText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.typeText = DirectLabel(parent=self, text='', pos=(0.12, 0, -0.075), text_scale=0.045)
        self.healthBar = SuitHealthBar.SuitHealthBar()
        self.generateHealthBar()
        self.suit = None
        self.suitHead = None
        self.hide()
        gui.removeNode()
    
    def cleanup(self):
        self.ignoreAll()
        self.cleanupHead()
        self.levelText.removeNode()
        self.typeText.removeNode()
        self.healthBar.delete()
        del self.levelText
        del self.typeText
        del self.healthBar
        DirectFrame.destroy(self)
    
    def cleanupHead(self):
        if self.suitHead:
            self.suitHead.removeNode()
            del self.suitHead

    def setSuit(self, suit):
        if self.suit == suit:
            messenger.send(self.suit.uniqueName('hpChange'))
            return

        self.ignoreAll()
        self.cleanupHead()
        self.suit = suit
        self.generateSuitHead(suit.getStyleName())
        self.updateHealthBar()
        self.levelText['text'] = TTLocalizer.CogPanelLevel % suit.getActualLevel()
        self.typeText['text'] = suit.getTypeText()
        self.accept(suit.uniqueName('hpChange'), self.updateHealthBar)

    def generateSuitHead(self, name):
        self.suitHead = Suit.attachSuitHead(self, name)
        self.suitHead.setScale(0.05)
        self.suitHead.setPos(0.1, 0, 0.01)
        
    def generateHealthBar(self):
        self.healthBar.generate()
        self.healthBar.geom.reparentTo(self)
        self.healthBar.geom.setScale(0.5)
        self.healthBar.geom.setPos(-0.065, 0, 0.05)
        self.healthBar.geom.show()

    def updateHealthBar(self):
        if not self.suit:
            return

        self.healthBar.update(float(self.suit.getHP()) / float(self.suit.getMaxHP()))