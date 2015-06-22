from toontown.toonbase import ToontownGlobals, TTLocalizer

Holidays = {
    ToontownGlobals.LAUGHING_MAN: {
        'startMonth': 6,
        'startDay': 22,
        'endMonth': 6,
        'endDay': 22,
        'startMessage': TTLocalizer.LaughingManHolidayStart,
        'ongoingMessage': TTLocalizer.LaughingManHolidayOngoing,
        'endMessage': TTLocalizer.LaughingManHolidayEnd
    },
    ToontownGlobals.GRAND_PRIX: {
        'weekDay': 0,
        'startMessage': TTLocalizer.CircuitRaceStart,
        'ongoingMessage': TTLocalizer.CircuitRaceOngoing,
        'endMessage': TTLocalizer.CircuitRaceEnd
    },
    ToontownGlobals.FISH_BINGO: {
        'weekDay': 2,
        'startMessage': TTLocalizer.FishBingoStart,
        'ongoingMessage': TTLocalizer.FishBingoOngoing,
        'endMessage': TTLocalizer.FishBingoEnd
    },
    ToontownGlobals.SILLY_SATURDAY: {
        'weekDay': 5,
        'startMessage': TTLocalizer.SillySaturdayStart,
        'ongoingMessage': TTLocalizer.SillySaturdayOngoing,
        'endMessage': TTLocalizer.SillySaturdayEnd
    }
}

def getHoliday(id):
    return Holidays.get(id, {})