from ShtikerPage import ShtikerPage
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import TTLocalizerEnglish

class GroupPage(ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('GroupPage')
    
    def __init__(self):
        ShtikerPage.__init__(self)
        
    def load(self):
        ShtikerPage.load(self)
        
    def unload(self):
        SktikerPage.unload(self)
        
    def enter(self):
        ShtikerPage.enter(self)
        
    def exit(self):
        ShtikerPage.exit(self)
        
    def destroy(self):
        DirectFrame.destroy(self)

        
  def cleanupDialog(self, value=0):        
      self.confirmDialog.cleanup()

   def create(self):
                self.background = OnscreenImage(parent = render2d, image="phase_3.5/map/toontown_central_tutorial_palette_4amla_1.jpg")
