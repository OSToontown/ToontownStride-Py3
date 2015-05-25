from toontown.battle import BattleParticles

def createSnow(geom):
    snow = BattleParticles.loadParticleFile('snowdisk.ptf')
    snow.setPos(0, 0, 5)
    snowRender = geom.attachNewNode('snowRender')
    snowRender.setDepthWrite(0)
    snowRender.setBin('fixed', 1)

    return snow, snowRender