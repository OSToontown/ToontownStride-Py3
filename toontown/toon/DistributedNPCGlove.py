from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
import time

from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.effects import DustCloud
from toontown.nametag.NametagGlobals import *
from toontown.toonbase import TTLocalizer

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

    def disable(self):
        self.ignoreAll()
        self.nextCollision = 0
        DistributedNPCToonBase.disable(self)

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
        taskMgr.doMethodLater(15, self.reset, 'npcSleepTask-%s' % self.doId)
        self.popupPickColorGUI()

    def exitPickColor(self, task=None):
        taskMgr.remove('npcSleepTask-%s' % self.doId)

        if task is not None:
            return task.done

    def popupPickColorGUI(self):
        self.setChatAbsolute('', CFSpeech)
        self.setChatAbsolute("Hi fucker", CFSpeech)
        base.setCellsActive(base.bottomCells, 0)
        self.d_requestTransformation(8)

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

    def reset(self, task=None):
        self.fsm.request('off')
        base.cr.playGame.getPlace().setState('walk')
        base.setCellsActive(base.bottomCells, 1)

        if task is not None:
            return task.done