from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.DistributedDistrictAI import DistributedDistrictAI
import time

class ToontownDistrictAI(DistributedDistrictAI):
    notify = directNotify.newCategory('ToontownDistrictAI')
    created = 0

    def announceGenerate(self):
        DistributedDistrictAI.announceGenerate(self)

        # Remember the time of which this district was created:
        self.created = int(time.time())

        # We want to handle shard status queries so that a ShardStatusReceiver
        # being created after we're generated will know where we're at:
        self.air.netMessenger.accept('queryShardStatus', self, self.handleShardStatusQuery)

        # Send a shard status update with the information we have:
        status = {
            'available': bool(self.available),
            'name': self.name,
            'created': int(time.time())
        }
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])

        # Add a post remove shard status update in-case we go down:
        status = {'available': False}
        datagram = self.air.netMessenger.prepare('shardStatus', [self.air.ourChannel, status])
        self.air.addPostRemove(datagram)

    def handleShardStatusQuery(self):
        # Send a shard status update with the information we have:
        status = {
            'available': bool(self.available),
            'name': self.name,
            'created': int(time.time())
        }
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])

    def setName(self, name):
        DistributedDistrictAI.setName(self, name)

        # Send a shard status update containing our name:
        status = {'name': name}
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])

    def setAvailable(self, available):
        DistributedDistrictAI.setAvailable(self, available)

        # Send a shard status update containing our availability:
        status = {'available': bool(available)}
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])