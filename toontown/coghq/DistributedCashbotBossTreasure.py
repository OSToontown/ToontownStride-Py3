from toontown.safezone import DistributedTreasure
from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3
Models = {ToontownGlobals.ToonIslandCentral: 'phase_4/models/props/icecream',
 ToontownGlobals.RainbowRise: 'phase_6/models/props/starfish_treasure',
 ToontownGlobals.TheBrrrgh: 'phase_8/models/props/snowflake_treasure',
 ToontownGlobals.MinniesMelodyland: 'phase_6/models/props/music_treasure',
 ToontownGlobals.DaisyGarden: 'phase_8/models/props/flower_treasure',
 ToontownGlobals.DonaldsDreamland: 'phase_8/models/props/zzz_treasure'}

class DistributedCashbotBossTreasure(DistributedTreasure.DistributedTreasure):
    pass # TBD
