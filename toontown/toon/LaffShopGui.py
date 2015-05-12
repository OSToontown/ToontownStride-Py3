from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.task.Task import Task
from toontown.toonbase import ToontownTimer
import LaffRestockGlobals
from LaffMeter import LaffMeter

class LaffShopGui(DirectFrame):

    def __init__(self, text):
        DirectFrame.__init__(
            self,
            parent=aspect2d,
            relief=None,
            geom=DGG.getDefaultDialogGeom(),
            geom_color=ToontownGlobals.GlobalDialogColor,
            geom_scale=(1.33, 1, 1.1),
            pos=(0, 0, 0),
            text=text,
            text_scale=0.07,
            text_pos=(0, 0.475),
        )
        self.initialiseoptions(LaffShopGui)
        self.text = text
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(aspect2d)
        self.timer.posInTopRightCorner()
        self.timer.accept('RESET_LAFFSHOP_TIMER', self.__resetTimer)
        self.timer.countdown(LaffRestockGlobals.LAFFCLERK_TIMER, self.__timerExpired)
        self.hp = base.localAvatar.getHp()
        self.maxHp = base.localAvatar.getMaxHp()
        self.floorLimit = self.hp
        self.ceilLimit = 0
        money = base.localAvatar.getTotalMoney()
        while self.ceilLimit * ToontownGlobals.CostPerLaffRestock < money:
            self.ceilLimit += 1
        self.__additionalLaff = 0
        self.__setupButtons()
        self.__bindButtons()
        self.laffMeter = LaffMeter(base.localAvatar.style, self.hp, self.maxHp)
        self.laffMeter.reparentTo(self)
        self.laffMeter.setPos(0, 0, 0.15)
        self.laffMeter.setScale(0.13)
        self.__updateLaffMeter(0)

    def __setupButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        arrowGui = loader.loadModel('phase_3/models/gui/create_a_toon_gui')
        okImageList = (
            buttons.find('**/ChtBx_OKBtn_UP'),
            buttons.find('**/ChtBx_OKBtn_DN'),
            buttons.find('**/ChtBx_OKBtn_Rllvr'),
        )
        cancelImageList = (
            buttons.find('**/CloseBtn_UP'),
            buttons.find('**/CloseBtn_DN'),
            buttons.find('**/CloseBtn_Rllvr'),
        )
        arrowImageList = (
            arrowGui.find('**/CrtATn_R_Arrow_UP'),
            arrowGui.find('**/CrtATn_R_Arrow_DN'),
            arrowGui.find('**/CrtATn_R_Arrow_RLVR'),
            arrowGui.find('**/CrtATn_R_Arrow_UP'),
        )
        self.cancelButton = DirectButton(
            parent=self,
            relief=None,
            image=cancelImageList,
            pos=(-0.2, 0, -0.4),
            text=LaffRestockGlobals.GuiCancel,
            text_scale=0.06,
            text_pos=(0, -0.1),
            command=self.__cancel,
        )
        self.okButton = DirectButton(
            parent=self,
            relief=None,
            image=okImageList,
            pos=(0.2, 0, -0.4),
            text=LaffRestockGlobals.GuiOk,
            text_scale=0.06,
            text_pos=(0, -0.1),
            command=self.__requestLaff,
            extraArgs=[],
        )
        self.upArrow = DirectButton(
            parent=self,
            relief=None,
            image=arrowImageList,
            image_scale=(1, 1, 1),
            image3_color=Vec4(0.6, 0.6, 0.6, 0.25),
            pos=(0.2, 0, -0.165),
        )
        self.downArrow = DirectButton(
            parent=self,
            relief=None,
            image=arrowImageList,
            image_scale=(-1, 1, 1),
            image3_color=Vec4(0.6, 0.6, 0.6, 0.25),
            pos=(-0.2, 0, -0.165),
        )
        buttons.removeNode()
        arrowGui.removeNode()

    def __bindButtons(self):
        self.downArrow.bind(DGG.B1PRESS, self.__downButtonDown)
        self.downArrow.bind(DGG.B1RELEASE, self.__downButtonUp)
        self.upArrow.bind(DGG.B1PRESS, self.__upButtonDown)
        self.upArrow.bind(DGG.B1RELEASE, self.__upButtonUp)

    def destroy(self):
        self.ignoreAll()
        if self.timer:
            self.timer.destroy()
        taskMgr.remove(self.taskName('runCounter'))
        DirectFrame.destroy(self)

    def __resetTimer(self):
        if self.timer:
            self.timer.stop()
            self.timer.countdown(LaffRestockGlobals.LAFFCLERK_TIMER, self.__timerExpired)

    def __timerExpired(self):
        self.destroy()
        messenger.send('guiDone', [True])

    def __cancel(self):
        self.destroy()
        messenger.send('guiDone', [False])

    def __requestLaff(self):
        if self.timer:
            self.ignoreAll()
        self.destroy()
        cost = self.__additionalLaff * ToontownGlobals.CostPerLaffRestock
        messenger.send('restockLaff', [self.__additionalLaff, cost])
        messenger.send('guiDone', [False])

    def __updateLaffMeter(self, amt):
        hitLimit = 0
        self.__additionalLaff += amt
        newLaff = self.hp + self.__additionalLaff
        cost = self.__additionalLaff * ToontownGlobals.CostPerLaffRestock
        if newLaff <= self.floorLimit:
            self.downArrow['state'] = DGG.DISABLED
            hitLimit = 1
        else:
            self.downArrow['state'] = DGG.NORMAL
        if newLaff >= self.maxHp or self.__additionalLaff >= self.ceilLimit:
            self.upArrow['state'] = DGG.DISABLED
            hitLimit = 1
        else:
            self.upArrow['state'] = DGG.NORMAL
        self['text'] = TTLocalizer.RestockAskMessage % (self.__additionalLaff, cost)
        self.laffMeter.hp = newLaff
        self.laffMeter.start()
        return (hitLimit, newLaff, self.__additionalLaff)

    def __runCounter(self, task):
        if task.time - task.prevTime < task.delayTime:
            return Task.cont
        else:
            task.delayTime = max(0.05, task.delayTime * 0.75)
            task.prevTime = task.time
            hitLimit, laff, trans = self.__updateLaffMeter(task.delta)
            if hitLimit:
                return Task.done
            else:
                return Task.cont

    def __downButtonUp(self, event):
        messenger.send('wakeup')
        taskMgr.remove(self.taskName('runCounter'))

    def __downButtonDown(self, event):
        messenger.send('wakeup')
        task = Task(self.__runCounter)
        task.delayTime = 0.4
        task.prevTime = 0.0
        task.delta = -1
        hitLimit, laff, trans = self.__updateLaffMeter(task.delta)
        if not hitLimit:
            taskMgr.add(task, self.taskName('runCounter'))

    def __upButtonUp(self, event):
        messenger.send('wakeup')
        taskMgr.remove(self.taskName('runCounter'))

    def __upButtonDown(self, event):
        messenger.send('wakeup')
        task = Task(self.__runCounter)
        task.delayTime = 0.4
        task.prevTime = 0.0
        task.delta = 1
        hitLimit, laff, trans = self.__updateLaffMeter(task.delta)
        if not hitLimit:
            taskMgr.add(task, self.taskName('runCounter'))
