from panda3d.core import *

def makeCard(book=False):
    cardMaker = CardMaker('king-jake-cm')
    cardMaker.setHasUvs(1)
    cardMaker.setFrame(-0.5, 0.5, -0.5, 0.5)

    nodePath = NodePath('king-jake')
    nodePath.setBillboardPointEye()

    lmBase = nodePath.attachNewNode(cardMaker.generate())
    lmBase.setTexture(loader.loadTexture('phase_3/maps/kj_base.png'))
    lmBase.setY(-0.3)
    lmBase.setScale(0.845)
    lmBase.setTransparency(True)

    lmText = nodePath.attachNewNode(cardMaker.generate())
    lmText.setTexture(loader.loadTexture('phase_3/maps/kj_text.png'))
    lmText.setY(-0.301)
    lmText.setScale(0.845)
    lmText.setTransparency(True)
    lmText.hprInterval(10, (0, 0, -360)).loop()

    lmFace = nodePath.attachNewNode(cardMaker.generate())
    lmFace.setTexture(loader.loadTexture('phase_3/maps/lm_face.rgba'))
    lmFace.setY(-0.302)
    lmFace.setTransparency(True)

    return nodePath

def addHeadEffect(head, book=False):
    card = makeCard(book=book)
    card.setScale(1.45 if book else 2.5)
    card.setZ(0.05 if book else 0.5)

    for nodePath in head.getChildren():
        nodePath.hide()

    card.instanceTo(head)

def addToonEffect(toon):
    for lod in toon.getLODNames():
        addHeadEffect(toon.getPart('head', lod))
