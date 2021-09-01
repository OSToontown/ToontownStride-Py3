from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownGlobals import *
from direct.gui import OnscreenText

class BossHealthBar:
    def __init__(self, dept):
        self.titleColor = (1, 1, 1, 1)
        self.smallTitleText = OnscreenText.OnscreenText('', fg=self.titleColor, font=getSuitFont(), pos=(0.65, 0.9), scale=0.08, drawOrder=0, mayChange=1, bg=(0.5, 0.5, 0.5, 0.5), align=TextNode.ARight)
        self.smallTitleText.hide()
        self.dept = dept
        return

    def initialize(self):
        #print('Initializing Boss Health Bar...')
        self.smallTitleText.show()

    def update(self, hp, maxhp):
        self.smallTitleText.setText('%s / %s' % (str(hp), str(maxhp)))
        #print('Updating Boss HP Bar...')

    def cleanUp(self):
        if self.smallTitleText:
            self.smallTitleText.cleanup()
            self.smallTitleText = None