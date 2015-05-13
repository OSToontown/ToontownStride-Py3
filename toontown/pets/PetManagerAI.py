from toontown.toonbase import ToontownGlobals, TTLocalizer
import PetUtil, PetDNA, time, random

DAY = 24 * 60 * 60

def getDayId():
    return int(time.time() / DAY)

class PetManagerAI:
    NUM_DAILY_PETS = 10

    def __init__(self, air):
        self.air = air
        self.seeds = simbase.backups.load('pet-seeds', (self.air.districtId,), default={})
        
        if self.seeds.get('day', -1) != getDayId():
            self.generateSeeds()

    def generateSeeds(self):
        seeds = range(0, 255)
        random.shuffle(seeds)

        self.seeds = {}
        for hood in (ToontownGlobals.ToontownCentral, ToontownGlobals.DonaldsDock, ToontownGlobals.DaisyGardens,
                     ToontownGlobals.MinniesMelodyland, ToontownGlobals.TheBrrrgh, ToontownGlobals.DonaldsDreamland):
            self.seeds[hood] = [seeds.pop() for _ in xrange(self.NUM_DAILY_PETS)]

        self.seeds['day'] = getDayId()
        simbase.backups.save('pet-seeds', (self.air.districtId,), self.seeds)

    def getAvailablePets(self, safezoneId):
        if self.seeds.get('day', -1) != getDayId():
            self.generateSeeds()

        return self.seeds[safezoneId] if safezoneId in self.seeds else self.seeds[str(safezoneId)]

    def createNewPetFromSeed(self, avId, seed, nameIndex, gender, safeZoneId):
        av = self.air.doId2do[avId]

        name = TTLocalizer.getPetName(nameIndex)
        _, dna, traitSeed = PetUtil.getPetInfoFromSeed(seed, safeZoneId)
        head, ears, nose, tail, body, color, cs, eye, _ = dna
        numGenders = len(PetDNA.PetGenders)
        gender %= numGenders

        fields = {'setOwnerId' : avId, 'setPetName' : name, 'setTraitSeed' : traitSeed, 'setSafeZone' : safeZoneId,
                  'setHead' : head, 'setEars' : ears, 'setNose' : nose, 'setTail' : tail, 'setBodyTexture' : body,
                  'setColor' : color, 'setColorScale' : cs, 'setEyeColor' : eye, 'setGender' : gender}

        def response(doId):
            if not doId:
                self.air.notify.warning("Cannot create pet for %s!" % avId)
                return

            self.air.writeServerEvent('bought-pet', avId, doId)
            av.b_setPetId(doId)

        self.air.dbInterface.createObject(self.air.dbId, self.air.dclassesByName['DistributedPetAI'],
                                          {k: (v,) for k,v in fields.items()}, response)

    def deleteToonsPet(self, avId):
        av = self.air.doId2do[avId]
        pet = av.getPetId()
        if pet:
            if pet in self.air.doId2do:
                self.air.doId2do[pet].requestDelete()
        av.b_setPetId(0)