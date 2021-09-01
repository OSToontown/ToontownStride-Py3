from panda3d.core import DecalEffect, NodePath
from direct.actor.Actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import State
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toon import Toon
from .SpotlightController import SpotlightController
from . import FatalInterior, FactoryExterior, FactoryInterior, SellbotHQExterior, SellbotHQBossBattle, CogHQLoader

aspectSF = 0.7227


class SellbotCogHQLoader(CogHQLoader.CogHQLoader):
    notify = DirectNotifyGlobal.directNotify.newCategory('SellbotCogHQLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        self.fsm.addState(State.State('factoryExterior', self.enterFactoryExterior, self.exitFactoryExterior,
                                      ['quietZone', 'factoryInterior', 'fatalInterior', 'cogHQExterior']))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('factoryExterior')

        self.fsm.addState(State.State('factoryInterior', self.enterFactoryInterior, self.exitFactoryInterior,
                                      ['quietZone', 'factoryExterior']))
        self.fsm.addState(State.State('fatalInterior', self.enterFatalInterior, self.exitFatalInterior,
                                      ['quietZone', 'factoryExterior']))
        for stateName in ['quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('factoryInterior')
            state.addTransition('fatalInterior')

        self.musicFile = 'phase_9/audio/bgm/encntr_suit_HQ_nbrhood.ogg'
        self.cogHQExteriorModelPath = 'phase_9/models/cogHQ/SellbotHQExterior'
        self.cogHQLobbyModelPath = 'phase_9/models/cogHQ/SellbotHQLobby'
        self.factoryExteriorModelPath = 'phase_9/models/cogHQ/SellbotFactoryExterior'
        self.geom = None
        self.spotlightController = None

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        Toon.loadSellbotHQAnims()

    def unloadPlaceGeom(self):
        self.stopSpotlights()
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        CogHQLoader.CogHQLoader.unloadPlaceGeom(self)

    def stopSpotlights(self):
        if self.spotlightController:
            self.spotlightController.delete()
            self.spotlightController = None

    def loadPlaceGeom(self, zoneId):
        zoneId = zoneId - zoneId % 100
        self.stopSpotlights()
        if zoneId == ToontownGlobals.SellbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)
            factoryPov = loader.loadModel('phase_9/models/cogHQ/SellbotFactoryPov')
            factoryPov.reparentTo(self.geom)
            factoryPov.setPosHpr(580.62, -139.52, 15.22, 272.73, 0, 0)
            dgLinkTunnel = self.geom.find('**/Tunnel1')
            dgLinkTunnel.setName('linktunnel_dg_5316_DNARoot')
            factoryLinkTunnel = self.geom.find('**/Tunnel2')
            factoryLinkTunnel.setName('linktunnel_sellhq_11200_DNARoot')
            cogSignModel = loader.loadModel('phase_4/models/props/sign_sellBotHeadHQ')
            cogSign = cogSignModel.find('**/sign_sellBotHeadHQ').copyTo(NodePath())
            cogSign.flattenStrong()
            cogSignModel.removeNode()
            cogSignSF = 23
            dgSign = cogSign.copyTo(dgLinkTunnel)
            dgSign.setPosHprScale(0.0, -291.5, 29, 180.0, 0.0, 0.0, cogSignSF, cogSignSF, cogSignSF * aspectSF)
            dgSign.node().setEffect(DecalEffect.make())
            dgText = DirectGui.OnscreenText(text=TTLocalizer.DaisyGarden[(-1)], font=ToontownGlobals.getSuitFont(),
                                            pos=(0,
                                                 -0.3), scale=TTLocalizer.SCHQLdgText, mayChange=False, parent=dgSign)
            dgText.setDepthWrite(0)
            dgText.flattenStrong()
            factorySign = cogSign.copyTo(factoryLinkTunnel)
            factorySign.setPosHprScale(148.625, -155, 27, -90.0, 0.0, 0.0, cogSignSF, cogSignSF, cogSignSF * aspectSF)
            factorySign.node().setEffect(DecalEffect.make())
            factoryTypeText = DirectGui.OnscreenText(text=TTLocalizer.Sellbot, font=ToontownGlobals.getSuitFont(),
                                                     pos=TTLocalizer.SellbotFactoryPosPart1,
                                                     scale=TTLocalizer.SellbotFactoryScalePart1, mayChange=False,
                                                     parent=factorySign)
            factoryTypeText.setDepthWrite(0)
            factoryTypeText.flattenStrong()
            factoryText = DirectGui.OnscreenText(text=TTLocalizer.Factory, font=ToontownGlobals.getSuitFont(),
                                                 pos=TTLocalizer.SellbotFactoryPosPart2,
                                                 scale=TTLocalizer.SellbotFactoryScalePart2, mayChange=False,
                                                 parent=factorySign)
            factoryText.setDepthWrite(0)
            factoryText.flattenStrong()
            doors = self.geom.find('**/doors')
            door0 = doors.find('**/door_0')
            door1 = doors.find('**/door_1')
            door2 = doors.find('**/door_2')
            door3 = doors.find('**/door_3')
            for door in [door0, door1, door2, door3]:
                doorFrame = door.find('**/doorDoubleFlat/+GeomNode')
                door.find('**/doorFrameHoleLeft').wrtReparentTo(doorFrame)
                door.find('**/doorFrameHoleRight').wrtReparentTo(doorFrame)
                doorTrigger = door.find('**/door_trigger*')
                doorTrigger.setY(doorTrigger.getY() - 1.5)
                doorFrame.node().setEffect(DecalEffect.make())
                doorFrame.flattenStrong()
                door.flattenMedium()

            cogSign.removeNode()
            self.geom.flattenMedium()
            self.spotlightController = SpotlightController()
            self.spotlightController.start(self.geom.find('**/SpotLights').getChildren())
        elif zoneId == ToontownGlobals.SellbotFactoryExt:
            self.geom = loader.loadModel(self.factoryExteriorModelPath)
            towers = loader.loadModel('phase_9/models/cogHQ/SellbotHQTowers')
            towers.reparentTo(self.geom)
            towers.setPosHpr(-148, -665, -10, 88, 0, 0)
            factoryLinkTunnel = self.geom.find('**/tunnel_group2')
            factoryLinkTunnel.setName('linktunnel_sellhq_11000_DNARoot')
            factoryLinkTunnel.find('**/tunnel_sphere').setName('tunnel_trigger')
            cogSignModel = loader.loadModel('phase_4/models/props/sign_sellBotHeadHQ')
            cogSign = cogSignModel.find('**/sign_sellBotHeadHQ').copyTo(NodePath())
            cogSign.flattenStrong()
            cogSignModel.removeNode()
            cogSignSF = 23
            elevatorSignSF = 15
            hqSign = cogSign.copyTo(factoryLinkTunnel)
            hqSign.setPosHprScale(0.0, -353, 27.5, -180.0, 0.0, 0.0, cogSignSF, cogSignSF, cogSignSF * aspectSF)
            hqSign.node().setEffect(DecalEffect.make())
            hqTypeText = DirectGui.OnscreenText(text=TTLocalizer.Sellbot, font=ToontownGlobals.getSuitFont(), pos=(0,
                                                                                                                   -0.25),
                                                scale=0.075, mayChange=False, parent=hqSign)
            hqTypeText.setDepthWrite(0)
            hqTypeText.flattenStrong()
            hqText = DirectGui.OnscreenText(text=TTLocalizer.Headquarters, font=ToontownGlobals.getSuitFont(), pos=(0,
                                                                                                                    -0.34),
                                            scale=0.1, mayChange=False, parent=hqSign)
            hqText.setDepthWrite(0)
            hqText.flattenStrong()
            frontDoor = self.geom.find('**/doorway1')
            fdSign = cogSign.copyTo(frontDoor)
            fdSign.setPosHprScale(62.74, -87.99, 17.26, 2.72, 0.0, 0.0, elevatorSignSF, elevatorSignSF,
                                  elevatorSignSF * aspectSF)
            fdSign.node().setEffect(DecalEffect.make())
            fdTypeText = DirectGui.OnscreenText(text=TTLocalizer.Factory, font=ToontownGlobals.getSuitFont(), pos=(0,
                                                                                                                   -0.25),
                                                scale=TTLocalizer.SCHQLfdTypeText, mayChange=False, parent=fdSign)
            fdTypeText.setDepthWrite(0)
            fdTypeText.flattenStrong()
            fdText = DirectGui.OnscreenText(text=TTLocalizer.SellbotFrontEntrance, font=ToontownGlobals.getSuitFont(),
                                            pos=(0,
                                                 -0.34), scale=TTLocalizer.SCHQLdgText, mayChange=False, parent=fdSign)
            fdText.setDepthWrite(0)
            fdText.flattenStrong()
            sideDoor = self.geom.find('**/doorway2')
            sdSign = cogSign.copyTo(sideDoor)
            sdSign.setPosHprScale(-164.78, 26.28, 17.25, -89.89, 0.0, 0.0, elevatorSignSF, elevatorSignSF,
                                  elevatorSignSF * aspectSF)
            sdSign.node().setEffect(DecalEffect.make())
            sdTypeText = DirectGui.OnscreenText(text=TTLocalizer.Factory, font=ToontownGlobals.getSuitFont(), pos=(0,
                                                                                                                   -0.25),
                                                scale=0.075, mayChange=False, parent=sdSign)
            sdTypeText.setDepthWrite(0)
            sdTypeText.flattenStrong()
            sdText = DirectGui.OnscreenText(text=TTLocalizer.SellbotSideEntrance, font=ToontownGlobals.getSuitFont(),
                                            pos=(0,
                                                 -0.34), scale=0.1, mayChange=False, parent=sdSign)
            sdText.setDepthWrite(0)
            sdText.flattenStrong()
            fatalDoor = self.geom.find('**/sign_origin')
            fatalSign = cogSign.copyTo(fatalDoor)
            fatalSign.setPosHprScale(0, 1.25, 4, 180, 0, 0, elevatorSignSF, elevatorSignSF, elevatorSignSF * aspectSF)
            fatalSign.node().setEffect(DecalEffect.make())
            fatalTypeText = TTLocalizer.Factory
            fatalTypeText = DirectGui.OnscreenText(text=fatalTypeText, font=ToontownGlobals.getSuitFont(), pos=(0,
                                                                                                                -0.25),
                                                   scale=0.075, mayChange=False, parent=fatalSign)
            fatalTypeText.setDepthWrite(0)
            fatalTypeText.flattenStrong()
            fatalText = TTLocalizer.SellbotFatalEntrance
            fatalText = DirectGui.OnscreenText(text=fatalText, font=ToontownGlobals.getSuitFont(), pos=(0,
                                                                                                        -0.34),
                                               scale=0.1, mayChange=False, parent=fatalSign)
            fatalText.setDepthWrite(0)
            fatalText.flattenStrong()

            cogSign.removeNode()
            self.geom.flattenMedium()
        elif zoneId == ToontownGlobals.SellbotLobby:
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)
            front = self.geom.find('**/frontWall')
            front.node().setEffect(DecalEffect.make())
            door = self.geom.find('**/door_0')
            parent = door.getParent()
            door.wrtReparentTo(front)
            doorFrame = door.find('**/doorDoubleFlat/+GeomNode')
            door.find('**/doorFrameHoleLeft').wrtReparentTo(doorFrame)
            door.find('**/doorFrameHoleRight').wrtReparentTo(doorFrame)
            doorFrame.node().setEffect(DecalEffect.make())
            door.find('**/leftDoor').wrtReparentTo(parent)
            door.find('**/rightDoor').wrtReparentTo(parent)
            self.geom.flattenStrong()
        else:
            self.notify.warning('loadPlaceGeom: unclassified zone %s' % zoneId)
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId)

    def unload(self):
        CogHQLoader.CogHQLoader.unload(self)
        Toon.unloadSellbotHQAnims()

    def enterFactoryExterior(self, requestStatus):
        self.placeClass = FactoryExterior.FactoryExterior
        self.enterPlace(requestStatus)
        self.hood.spawnTitleText(requestStatus['zoneId'])

    def exitFactoryExterior(self):
        taskMgr.remove('titleText')
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None

    def enterFatalInterior(self, requestStatus):
        self.placeClass = FatalInterior.FatalInterior
        self.enterPlace(requestStatus)

    def exitFatalInterior(self):
        self.exitPlace()
        self.placeClass = None

    def enterFactoryInterior(self, requestStatus):
        self.placeClass = FactoryInterior.FactoryInterior
        self.enterPlace(requestStatus)

    def exitFactoryInterior(self):
        self.exitPlace()
        self.placeClass = None

    def getExteriorPlaceClass(self):
        return SellbotHQExterior.SellbotHQExterior

    def getBossPlaceClass(self):
        return SellbotHQBossBattle.SellbotHQBossBattle