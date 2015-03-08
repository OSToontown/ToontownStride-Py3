from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
import time

from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.effects import DustCloud
from toontown.nametag.NametagGlobals import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon.ToonDNA import allColorsList

def getDustCloud(toon):
    dustCloud = DustCloud.DustCloud(fBillboard=0)
    
    dustCloud.setBillboardAxis(2.0)
    dustCloud.setZ(3)
    dustCloud.setScale(0.4)
    dustCloud.createTrack()
    return Sequence(Wait(0.5), Func(dustCloud.reparentTo, toon), dustCloud.track, Func(dustCloud.destroy))

class DistributedNPCGlove(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.nextCollision = 0

        self.fsm = ClassicFSM.ClassicFSM(
            'NPCGlove',
            [
                State.State('off', self.enterOff, self.exitOff, ['pickColor']),
                State.State('pickColor', self.enterPickColor, self.exitPickColor, ['off'])
            ], 'off', 'off')
        self.fsm.enterInitialState()
        
        self.title = None
        self.notice = None
        self.color = None
        self.buyButton = None
        self.cancelButton = None
        self.leftButton = None
        self.rightButton = None
        self.index = 0
        
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        self.shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        self.shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        self.shuffleUp = self.gui.find('**/tt_t_gui_mat_shuffleUp')
        self.shuffleDown = self.gui.find('**/tt_t_gui_mat_shuffleDown')

    def disable(self):
        self.ignoreAll()
        self.destroyGui()
        self.nextCollision = 0
        DistributedNPCToonBase.disable(self)
    
    def destroyGui(self):
        for element in [self.title, self.notice, self.color, self.buyButton, self.cancelButton, self.leftButton, self.rightButton]:
            if element:
                element.destroy()
                element = None
        
        self.index = 0
    
    def createGui(self):
        self.title = DirectLabel(aspect2d, relief=None, text=TTLocalizer.GloveGuiTitle,
                     text_fg=(0, 1, 0, 1), text_scale=0.21, text_font=ToontownGlobals.getSignFont(),
                     pos=(0, 0, -0.30), text_shadow=(1, 1, 1, 1))
        
        self.notice = DirectLabel(aspect2d, relief=None, text=TTLocalizer.GloveGuiNotice % ToontownGlobals.GloveCost,
                      text_fg=(1, 0, 0, 1), text_scale=0.11, text_font=ToontownGlobals.getSignFont(),
                      pos=(0, 0, -0.45), text_shadow=(1, 1, 1, 1))
        
        self.color = DirectLabel(aspect2d, relief=None, text='',
                     text_scale=0.11, text_font=ToontownGlobals.getSignFont(),
                     pos=(0, 0, -0.70), text_shadow=(1, 1, 1, 1))
        
        self.buyButton = DirectButton(aspect2d, relief=None, image=(self.shuffleUp, self.shuffleDown),
                         text=TTLocalizer.GloveGuiBuy, text_font=ToontownGlobals.getInterfaceFont(),
                         text_scale=0.11, text_pos=(0, -0.02), pos=(-0.60, 0, -0.90), text_fg=(1, 1, 1, 1),
                         text_shadow=(0, 0, 0, 1), command=self.handleBuy)
        
        self.cancelButton = DirectButton(aspect2d, relief=None, image=(self.shuffleUp, self.shuffleDown),
                            text=TTLocalizer.GloveGuiCancel, text_font=ToontownGlobals.getInterfaceFont(),
                            text_scale=0.11, text_pos=(0, -0.02), pos=(0.60, 0, -0.90), text_fg=(1, 1, 1, 1),
                            text_shadow=(0, 0, 0, 1), command=self.leave)
        
        self.leftButton = DirectButton(aspect2d, relief=None, image=(self.shuffleArrowUp, self.shuffleArrowDown),
                          pos=(-0.60, 0, -0.66), command=self.handleSetIndex, extraArgs=[-1])

        self.rightButton = DirectButton(aspect2d, relief=None, image=(self.shuffleArrowUp, self.shuffleArrowDown),
                           pos=(0.60, 0, -0.66), scale=-1, command=self.handleSetIndex, extraArgs=[1])
        
        self.updateGuiByIndex()

    def handleSetIndex(self, offset):
        newIndex = self.index + offset
        
        if newIndex > -1 and newIndex < len(TTLocalizer.NumToColor):
            self.index = newIndex
            self.updateGuiByIndex()
    
    def updateGuiByIndex(self):
        self.color['text'] = TTLocalizer.NumToColor[self.index]
        self.color['text_fg'] = allColorsList[self.index]
    
    def handleBuy(self):
        self.d_requestTransformation(self.index)
    
    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        self.setPosHpr(101, -14, 4, -305, 0, 0)

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        self.currentTime = time.time()

        if self.nextCollision <= self.currentTime:
            self.fsm.request('pickColor')

        self.nextCollision = self.currentTime + 2

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterPickColor(self):
        base.cr.playGame.getPlace().setState('stopped')
        taskMgr.doMethodLater(45, self.leave, 'npcSleepTask-%s' % self.doId)
        self.setChatAbsolute('', CFSpeech)
        
        if base.localAvatar.getMoney() < ToontownGlobals.GloveCost:
            self.setChatAbsolute(self.getMessageById(2), CFSpeech|CFTimeout)
            self.reset()
        else:
            self.popupPickColorGUI()

    def exitPickColor(self, task=None):
        taskMgr.remove('npcSleepTask-%s' % self.doId)
        taskMgr.doMethodLater(0.5, self.reset, 'avatarRecover-%s-%s' % (self.doId, base.localAvatar.doId))
        
        if task is not None:
            return task.done

    def popupPickColorGUI(self):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.GlovePickColorMessage, CFSpeech)
        base.setCellsActive(base.bottomCells, 0)
        self.createGui()

    def getMessageById(self, response):
        if response == 1:
            return TTLocalizer.GloveSameColorMessage
        elif response == 2:
            return TTLocalizer.GloveNoMoneyMessage
        else:
            return TTLocalizer.GloveSuccessMessage

    def doTransformation(self, avId, response):
        av = self.cr.doId2do.get(avId)
        
        if not av:
            return
            
        if response == 3:
            getDustCloud(av).start()

        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(self.getMessageById(response), CFSpeech|CFTimeout)

    def d_requestTransformation(self, color):
        self.sendUpdate('requestTransformation', [color])
        self.reset()

    def leave(self):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute(TTLocalizer.GloveByeMessage, CFSpeech|CFTimeout)
        self.reset()
    
    def reset(self, task=None):
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')
        base.setCellsActive(base.bottomCells, 1)
        self.destroyGui()

        if task is not None:
            return task.done