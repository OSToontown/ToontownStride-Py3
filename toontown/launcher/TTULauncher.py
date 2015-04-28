from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import os, sys, time, argparse

class LogAndOutput:
    def __init__(self, orig, log):
        self.orig = orig
        self.log = log

    def write(self, str):
        self.log.write(str)
        self.log.flush()
        self.orig.write(str)
        self.orig.flush()

    def flush(self):
        self.log.flush()
        self.orig.flush()

class TTULauncher:
    notify = DirectNotifyGlobal.directNotify.newCategory('TTULauncher')

    def __init__(self):
        self.logPrefix = 'united-'
        self.http = HTTPClient()
        
        parser = argparse.ArgumentParser()
        parser.add_argument('token')
        parser.add_argument('server')
        self.args = parser.parse_args()

        ltime = 1 and time.localtime()
        logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000,  ltime[1], ltime[2], ltime[3], ltime[4], ltime[5])

        if not os.path.exists('logs/'):
            os.mkdir('logs/')
            self.notify.info('Made new directory to save logs.')

        logfile = os.path.join('logs', self.logPrefix + logSuffix + '.log')

        log = open(logfile, 'a')
        logOut = LogAndOutput(sys.stdout, log)
        logErr = LogAndOutput(sys.stderr, log)
        sys.stdout = logOut
        sys.stderr = logErr

    def getPlayToken(self):
        return self.args.token

    def getGameServer(self):
        return self.args.server
    
    def setPandaErrorCode(self):
        pass
    
    def setDisconnectDetails(self, disconnectCode, disconnectMsg):
        self.disconnectCode = disconnectCode
        self.disconnectMsg = disconnectMsg
    
    def setDisconnectDetailsNormal(self):
        self.setDisconnectDetails(0, 'normal')
