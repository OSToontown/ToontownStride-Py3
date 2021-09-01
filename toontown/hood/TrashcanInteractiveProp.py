from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import InteractiveAnimatedProp
from toontown.toonbase import ToontownGlobals, ToontownBattleGlobals, TTLocalizer

class TrashcanInteractiveProp(InteractiveAnimatedProp.InteractiveAnimatedProp):
    notify = DirectNotifyGlobal.directNotify.newCategory('TrashcanInteractiveProp')
    BattleTrack = ToontownBattleGlobals.HEAL_TRACK
    BattleCheerText = TTLocalizer.InteractivePropTrackBonusTerms[BattleTrack]

    ZoneToIdles = {
        ToontownGlobals.ToonIslandCentral: (('tt_a_ara_ttc_trashcan_idleTake2', 1, 1, None, 3, 10),
                                         ('tt_a_ara_ttc_trashcan_idleHiccup0', 1, 1, None, 3, 10),
                                         ('tt_a_ara_ttc_trashcan_idleLook1', 1, 1, None, 3, 10),
                                         ('tt_a_ara_ttc_trashcan_idleAwesome3', 1, 1, None, 3, 10)),
        ToontownGlobals.RainbowRise: (('tt_a_ara_dod_trashcan_idleBounce2', 3, 10, 'tt_a_ara_dod_trashcan_idle0settle', 3, 10),
                                     ('tt_a_ara_dod_trashcan_idle0', 1, 1, None, 3, 10),
                                     ('tt_a_ara_dod_trashcan_idle1', 1, 1, None, 3, 10),
                                     ('tt_a_ara_dod_trashcan_idleAwesome3', 1, 1, None, 3, 10)),
        ToontownGlobals.DaisyGarden: (('tt_a_ara_dga_trashcan_idleTake2', 1, 1, None, 3, 10),
                                      ('tt_a_ara_dga_trashcan_idleHiccup0', 1, 1, None, 3, 10),
                                      ('tt_a_ara_dga_trashcan_idleLook1', 1, 1, None, 3, 10),
                                      ('tt_a_ara_dga_trashcan_idleAwesome3', 1, 1, None, 3, 10)),
        ToontownGlobals.MinniesMelodyland: (('tt_a_ara_mml_trashcan_idleBounce0', 3, 10, 'tt_a_ara_mml_trashcan_idle0settle', 3, 10),
                                           ('tt_a_ara_mml_trashcan_idleLook1', 1, 1, None, 3, 10),
                                           ('tt_a_ara_mml_trashcan_idleHelicopter2', 1, 1, None, 3, 10),
                                           ('tt_a_ara_mml_trashcan_idleAwesome3', 1, 1, None, 3, 10)),
        ToontownGlobals.TheBrrrgh: (('tt_a_ara_tbr_trashcan_idleShiver1', 1, 1, None, 3, 10),
                                   ('tt_a_ara_tbr_trashcan_idleSneeze2', 1, 1, None, 3, 10),
                                   ('tt_a_ara_tbr_trashcan_idle0', 1, 1, None, 3, 10),
                                   ('tt_a_ara_tbr_trashcan_idleAwesome3', 1, 1, None, 3, 10)),
        ToontownGlobals.DonaldsDreamland: (('tt_a_ara_ddl_trashcan_idleSleep0', 3, 10, None, 0, 0),
                                          ('tt_a_ara_ddl_trashcan_idleShake2', 1, 1, None, 0, 0),
                                          ('tt_a_ara_ddl_trashcan_idleSnore1', 1, 1, None, 0, 0),
                                          ('tt_a_ara_ddl_trashcan_idleAwesome3', 1, 1, None, 0, 0))}

    ZoneToIdleIntoFightAnims = {
        ToontownGlobals.ToonIslandCentral: 'tt_a_ara_ttc_trashcan_idleIntoFight',
        ToontownGlobals.RainbowRise: 'tt_a_ara_dod_trashcan_idleIntoFight',
        ToontownGlobals.DaisyGarden: 'tt_a_ara_dga_trashcan_idleIntoFight',
        ToontownGlobals.MinniesMelodyland: 'tt_a_ara_mml_trashcan_idleIntoFight',
        ToontownGlobals.TheBrrrgh: 'tt_a_ara_tbr_trashcan_idleIntoFight',
        ToontownGlobals.DonaldsDreamland: 'tt_a_ara_ddl_trashcan_idleIntoFight'}

    ZoneToVictoryAnims = {
        ToontownGlobals.ToonIslandCentral: 'tt_a_ara_ttc_trashcan_victoryDance',
        ToontownGlobals.RainbowRise: 'tt_a_ara_dod_trashcan_victoryDance',
        ToontownGlobals.DaisyGarden: 'tt_a_ara_dga_trashcan_victoryDance',
        ToontownGlobals.MinniesMelodyland: 'tt_a_ara_mml_trashcan_victoryDance',
        ToontownGlobals.TheBrrrgh: 'tt_a_ara_tbr_trashcan_victoryDance',
        ToontownGlobals.DonaldsDreamland: 'tt_a_ara_ddl_trashcan_victoryDance'}

    ZoneToSadAnims = {
        ToontownGlobals.ToonIslandCentral: 'tt_a_ara_ttc_trashcan_fightSad',
        ToontownGlobals.RainbowRise: 'tt_a_ara_dod_trashcan_fightSad',
        ToontownGlobals.DaisyGarden: 'tt_a_ara_dga_trashcan_fightSad',
        ToontownGlobals.MinniesMelodyland: 'tt_a_ara_mml_trashcan_fightSad',
        ToontownGlobals.TheBrrrgh: 'tt_a_ara_tbr_trashcan_fightSad',
        ToontownGlobals.DonaldsDreamland: 'tt_a_ara_ddl_trashcan_fightSad'}

    ZoneToFightAnims = {
        ToontownGlobals.ToonIslandCentral: ('tt_a_ara_ttc_trashcan_fightBoost', 'tt_a_ara_ttc_trashcan_fightCheer', 'tt_a_ara_ttc_trashcan_fightIdle'),
        ToontownGlobals.RainbowRise: ('tt_a_ara_dod_trashcan_fightBoost', 'tt_a_ara_dod_trashcan_fightCheer', 'tt_a_ara_dod_trashcan_fightIdle'),
        ToontownGlobals.DaisyGarden: ('tt_a_ara_dga_trashcan_fightBoost', 'tt_a_ara_dga_trashcan_fightCheer', 'tt_a_ara_dga_trashcan_fightIdle'),
        ToontownGlobals.MinniesMelodyland: ('tt_a_ara_mml_trashcan_fightBoost', 'tt_a_ara_mml_trashcan_fightCheer0', 'tt_a_ara_mml_trashcan_fightCheer1', 'tt_a_ara_mml_trashcan_fightIdle'),
        ToontownGlobals.TheBrrrgh: ('tt_a_ara_tbr_trashcan_fightBoost', 'tt_a_ara_tbr_trashcan_fightCheer', 'tt_a_ara_tbr_trashcan_fightIdle'),
        ToontownGlobals.DonaldsDreamland: ('tt_a_ara_ddl_trashcan_fightBoost', 'tt_a_ara_ddl_trashcan_fightCheer', 'tt_a_ara_ddl_trashcan_fightIdle')}

    IdlePauseTime = base.config.GetFloat('prop-idle-pause-time', 0.0)
