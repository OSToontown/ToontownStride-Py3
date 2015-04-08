from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.uberdog.ClientServicesManagerUD import executeHttpRequestAndLog

class TrueFriendsMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TrueFriendsMgrAI")

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def requestId(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        
        if not av:
            return

        if config.GetString('accountdb-type', 'developer') != 'remote':
            self.sendUpdateToAvatarId(avId, 'requestIdResult', [0, None, None])
            return
        
        result = executeHttpRequestAndLog('truefriend', avid=avId)
        
        if result is None:
            self.sendUpdateToAvatarId(avId, 'requestIdResult', [1, None, None])
            return
        elif 'error' in result:
            self.sendUpdateToAvatarId(avId, 'requestIdResult', [1, result['error'], None])
            return
        
        self.sendUpdateToAvatarId(avId, 'requestIdResult', [2, result['id'], result['expires']])
    
    def redeemId(self, id):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)

        if not av:
            return

        if simbase.config.GetString('accountdb-type', 'developer') != 'remote':
            self.sendUpdateToAvatarId(avId, 'redeemIdResult', [0, None])
            return
        
        result = executeHttpRequestAndLog('truefriend', id=id)
        
        if result is None:
            self.sendUpdateToAvatarId(avId, 'redeemIdResult', [1, None])
            return
        elif 'error' in result:
            self.sendUpdateToAvatarId(avId, 'redeemIdResult', [1, result['error']])
            return
        
        targetId = int(result['avId'])
        
        if targetId == avId:
            self.sendUpdateToAvatarId(avId, 'redeemIdResult', [2, None])
            return
        elif av.isTrueFriend(targetId):
            self.sendUpdateToAvatarId(avId, 'redeemIdResult', [3, None])
            return

        av.addTrueFriend(targetId)
        target = self.air.doId2do.get(targetId)
        
        if target:
            target.addTrueFriend(avId)
            self.sendUpdateToAvatarId(avId, 'redeemIdResult', [4, target.getName()])
        else:
            TrueFriendsOperation(targetId, avId)

class TrueFriendsOperation:

    def __init__(self, targetId, avId):
        self.targetId = targetId
        self.avId = avId
        simbase.air.dbInterface.queryObject(simbase.air.dbId, self.targetId, self.gotResponse)
    
    def gotResponse(self, dclass, fields):
        if dclass != simbase.air.dclassesByName['DistributedToonAI'] or not 'setName' in fields:
            return
        
        trueFriends = fields['setTrueFriends']
        
        if self.avId in trueFriends:
            self.sendUpdateToAvatarId(self.avId, 'redeemIdResult', [3, None])
            return
        
        trueFriends.append(self.avId)
        simbase.air.dbInterface.updateObject(simbase.air.dbId, self.targetId, simbase.air.dclassesByName['DistributedToonAI'], {'setTrueFriends': [trueFriends]})
        self.sendUpdateToAvatarId(self.avId, 'redeemIdResult', [4, fields['setName']])