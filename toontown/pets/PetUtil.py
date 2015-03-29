from toontown.pets import PetDNA, PetTraits, PetConstants
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil

def getPetInfoFromSeed(seed, safezoneId):
    dnaArray = PetDNA.getRandomPetDNA(seed, safezoneId)
    gender = PetDNA.getGender(dnaArray)
    nameString = TTLocalizer.getRandomPetName(gender=gender, seed=seed)
    traitSeed = PythonUtil.randUint31()
    return (nameString, dnaArray, traitSeed)


def getPetCostFromSeed(seed, safezoneId):
    name, dna, traitSeed = getPetInfoFromSeed(seed, safezoneId)
    traits = PetTraits.PetTraits(traitSeed, safezoneId)
    traitValue = traits.getOverallValue()
    traitValue -= 0.3
    traitValue = max(0, traitValue)
    rarity = PetDNA.getRarity(dna)
    rarity *= 1.0 - traitValue
    rarity = pow(0.001, rarity) - 0.001
    minCost, maxCost = PetConstants.ZoneToCostRange[safezoneId]
    cost = rarity * (maxCost - minCost) + minCost
    cost = int(cost)
    return cost
