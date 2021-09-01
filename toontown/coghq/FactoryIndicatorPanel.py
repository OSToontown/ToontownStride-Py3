from toontown.coghq import DistributedStageRoom
from toontown.hood import Hood
from toontown.hood import CashbotHQ
from toontown.hood import ZoneUtil

def spawnFacilityText(self, zoneId, floorNum=None):
    if ZoneUtil.isMintInteriorZone(zoneId):
        text = 'Floor %s' % (floorNum + 1)
        self.doSpawnFacilityText(text)
        return

    CogHood.spawnFacilityText(self, zoneId)