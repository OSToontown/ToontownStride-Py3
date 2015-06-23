from panda3d.core import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import ZoneUtil
import random

LOADING_SCREEN_SORT_INDEX = 4000

class ToontownLoadingScreen:

    def __init__(self):
        self.__expectedCount = 0
        self.__count = 0
        self.gui = loader.loadModel('phase_3/models/gui/progress-background.bam')
        self.title = DirectLabel(guiId='ToontownLoadingScreenTitle', parent=self.gui, relief=None, pos=(base.a2dRight/5, 0, 0.235), text='', textMayChange=1, text_scale=0.08, text_fg=(0, 0, 0.5, 1), text_align=TextNode.ALeft, text_font=ToontownGlobals.getInterfaceFont())
        self.tip = DirectLabel(guiId='ToontownLoadingScreenTip', parent=self.gui, relief=None, pos=(0, 0, 0.045), text='', textMayChange=1, text_scale=0.05, text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_align=TextNode.ACenter)
        self.waitBar = DirectWaitBar(guiId='ToontownLoadingScreenWaitBar', parent=self.gui, frameSize=(base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03), pos=(0, 0, 0.15), text='')
        logoScale = 0.5625  # Scale for our locked aspect ratio (2:1).
        self.logo = OnscreenImage(
            image='phase_3/maps/toontown-logo.png',
            scale=(logoScale * 2.0, 1, logoScale))
        self.logo.reparentTo(hidden)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        scale = self.logo.getScale()
        self.logo.setPos(0, 0, -scale[2])

    def destroy(self):
        self.tip.destroy()
        self.title.destroy()
        self.gui.removeNode()
        self.logo.removeNode()

    def getTip(self, tipCategory):
        return TTLocalizer.TipTitle + ' ' + random.choice(TTLocalizer.TipDict.get(tipCategory))

    def begin(self, range, label, gui, tipCategory, zoneId):
        self.defaultTex = 'phase_3.5/maps/loading/default.jpg'
        self.defaultFont = ToontownGlobals.getInterfaceFont()
        self.defaultFontColor = (0, 0, 0.5, 1)
        self.zone2picture = {
            ToontownGlobals.GoofySpeedway : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.ToontownCentral : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SillyStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LoopyLane : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.PunchlinePlace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.DonaldsDock : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.BarnacleBoulevard : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SeaweedStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LighthouseLane : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.DaisyGardens : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.ElmStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.MapleStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.OakStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.MinniesMelodyland : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.AltoAvenue : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.BaritoneBoulevard : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.TenorTerrace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.TheBrrrgh : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.WalrusWay : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SleetStreet : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.PolarPlace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.DonaldsDreamland : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.LullabyLane : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.PajamaPlace : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.OutdoorZone : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.GolfZone : 'phase_3.5/maps/loading/toon.jpg',
            ToontownGlobals.SellbotHQ : 'phase_3.5/maps/loading/cog.jpg',
            ToontownGlobals.SellbotFactoryExt : 'phase_3.5/maps/loading/cog.jpg',
            ToontownGlobals.SellbotFactoryInt : 'phase_3.5/maps/loading/cog.jpg',
            ToontownGlobals.SellbotMegaCorpInt : 'phase_3.5/maps/loading/cog.jpg',
            ToontownGlobals.CashbotHQ : 'phase_3.5/maps/loading/cog.jpg',
            ToontownGlobals.LawbotHQ : 'phase_3.5/maps/loading/cog.jpg',
            ToontownGlobals.BossbotHQ : 'phase_3.5/maps/loading/cog.jpg'
        }
        self.zone2font = {
            ToontownGlobals.GoofySpeedway : ToontownGlobals.getSignFont(),
            ToontownGlobals.ToontownCentral : ToontownGlobals.getSignFont(),
            ToontownGlobals.SillyStreet : ToontownGlobals.getSignFont(),
            ToontownGlobals.LoopyLane : ToontownGlobals.getSignFont(),
            ToontownGlobals.PunchlinePlace : ToontownGlobals.getSignFont(),
            ToontownGlobals.DonaldsDock : ToontownGlobals.getSignFont(),
            ToontownGlobals.BarnacleBoulevard : ToontownGlobals.getSignFont(),
            ToontownGlobals.SeaweedStreet : ToontownGlobals.getSignFont(),
            ToontownGlobals.LighthouseLane : ToontownGlobals.getSignFont(),
            ToontownGlobals.DaisyGardens : ToontownGlobals.getSignFont(),
            ToontownGlobals.ElmStreet : ToontownGlobals.getSignFont(),
            ToontownGlobals.MapleStreet : ToontownGlobals.getSignFont(),
            ToontownGlobals.OakStreet : ToontownGlobals.getSignFont(),
            ToontownGlobals.MinniesMelodyland : ToontownGlobals.getSignFont(),
            ToontownGlobals.AltoAvenue : ToontownGlobals.getSignFont(),
            ToontownGlobals.BaritoneBoulevard : ToontownGlobals.getSignFont(),
            ToontownGlobals.TenorTerrace : ToontownGlobals.getSignFont(),
            ToontownGlobals.TheBrrrgh : ToontownGlobals.getSignFont(),
            ToontownGlobals.WalrusWay : ToontownGlobals.getSignFont(),
            ToontownGlobals.SleetStreet : ToontownGlobals.getSignFont(),
            ToontownGlobals.PolarPlace : ToontownGlobals.getSignFont(),
            ToontownGlobals.DonaldsDreamland : ToontownGlobals.getSignFont(),
            ToontownGlobals.LullabyLane : ToontownGlobals.getSignFont(),
            ToontownGlobals.PajamaPlace : ToontownGlobals.getSignFont(),
            ToontownGlobals.OutdoorZone : ToontownGlobals.getSignFont(),
            ToontownGlobals.GolfZone : ToontownGlobals.getSignFont(),
            ToontownGlobals.SellbotHQ : ToontownGlobals.getSuitFont(),
            ToontownGlobals.SellbotFactoryExt : ToontownGlobals.getSuitFont(),
            ToontownGlobals.SellbotFactoryInt : ToontownGlobals.getSuitFont(),
            ToontownGlobals.SellbotMegaCorpInt : ToontownGlobals.getSuitFont(),
            ToontownGlobals.CashbotHQ : ToontownGlobals.getSuitFont(),
            ToontownGlobals.LawbotHQ : ToontownGlobals.getSuitFont(),
            ToontownGlobals.BossbotHQ : ToontownGlobals.getSuitFont()
        }
        self.zone2fontcolor = {
            ToontownGlobals.GoofySpeedway : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.ToontownCentral : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.SillyStreet : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.LoopyLane : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.PunchlinePlace : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.DonaldsDock : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.BarnacleBoulevard : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.SeaweedStreet : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.LighthouseLane : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.DaisyGardens : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.ElmStreet : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.MapleStreet : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.OakStreet : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.MinniesMelodyland : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.AltoAvenue : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.BaritoneBoulevard : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.TenorTerrace : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.TheBrrrgh : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.WalrusWay : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.SleetStreet : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.PolarPlace : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.DonaldsDreamland : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.LullabyLane : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.PajamaPlace : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.OutdoorZone : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.GolfZone : VBase4(0.2, 0.6, 0.9, 1.0),
            ToontownGlobals.SellbotHQ : (1.0, 1.0, 1.0, 1.0),
            ToontownGlobals.SellbotFactoryExt : (1.0, 1.0, 1.0, 1.0),
            ToontownGlobals.SellbotFactoryInt : (1.0, 1.0, 1.0, 1.0),
            ToontownGlobals.SellbotMegaCorpInt : (1.0, 1.0, 1.0, 1.0),
            ToontownGlobals.CashbotHQ : (1.0, 1.0, 1.0, 1.0),
            ToontownGlobals.LawbotHQ : (1.0, 1.0, 1.0, 1.0),
            ToontownGlobals.BossbotHQ : (1.0, 1.0, 1.0, 1.0)
        }

        self.waitBar['range'] = range
        self.title['text'] = label
        self.loadingScreenTex = self.zone2picture.get(ZoneUtil.getBranchZone(zoneId), self.defaultTex)
        self.loadingScreenFont = self.zone2font.get(ZoneUtil.getBranchZone(zoneId), self.defaultFont)
        self.loadingScreenFontColor = self.zone2fontcolor.get(ZoneUtil.getBranchZone(zoneId), self.defaultFontColor)
        self.background = loader.loadTexture(self.loadingScreenTex)
        self.__count = 0
        self.__expectedCount = range
        if gui:
            self.waitBar['frameSize'] = (base.a2dLeft+(base.a2dRight/4.95), base.a2dRight-(base.a2dRight/4.95), -0.03, 0.03)
            self.title['text_font'] = self.loadingScreenFont
            self.title['text_fg'] = self.loadingScreenFontColor
            self.title.reparentTo(base.a2dpBottomLeft, LOADING_SCREEN_SORT_INDEX)
            self.title.setPos(base.a2dRight/5, 0, 0.235)
            self.tip['text'] = self.getTip(tipCategory)
            self.gui.setPos(0, -0.1, 0)
            self.gui.reparentTo(aspect2d, LOADING_SCREEN_SORT_INDEX)
            self.gui.setTexture(self.background, 1)
            #if self.loadingScreenTex == self.defaultTex:
            #    self.logo.reparentTo(base.a2dpTopCenter, LOADING_SCREEN_SORT_INDEX)
            self.logo.reparentTo(base.a2dpTopCenter, LOADING_SCREEN_SORT_INDEX)
        else:
            self.title.reparentTo(base.a2dpBottomLeft, LOADING_SCREEN_SORT_INDEX)
            self.gui.reparentTo(hidden)
            self.logo.reparentTo(hidden)
        self.tip.reparentTo(base.a2dpBottomCenter, LOADING_SCREEN_SORT_INDEX)
        self.waitBar.reparentTo(base.a2dpBottomCenter, LOADING_SCREEN_SORT_INDEX)
        self.waitBar.update(self.__count)

    def end(self):
        self.waitBar.finish()
        self.waitBar.reparentTo(self.gui)
        self.title.reparentTo(self.gui)
        self.tip.reparentTo(self.gui)
        self.gui.reparentTo(hidden)
        self.logo.reparentTo(hidden)
        return (self.__expectedCount, self.__count)

    def abort(self):
        self.gui.reparentTo(hidden)

    def tick(self):
        self.__count = self.__count + 1
        self.waitBar.update(self.__count)
