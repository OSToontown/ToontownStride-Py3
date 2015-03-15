from direct.stdpy import threading

from libpandadna import *

class DNABulkLoader:
    def __init__(self, storage, files):
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print 'Reading DNA file...', file
            loadDNABulk(self.dnaStorage, file)
        del self.dnaStorage
        del self.dnaFiles

def loadDNABulk(dnaStorage, file):
    dnaLoader = DNALoader()
    fileu = '../resources/' + file
    fileo = 'resources/' + file
    try:
        dnaLoader.loadDNAFile(dnaStorage, fileu)
    except:
        dnaLoader.loadDNAFile(dnaStorage, fileo)

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader()
    fileu = '../resources/' + file
    fileo = 'resources/' + file
    try:
        node = dnaLoader.loadDNAFile(dnaStorage, fileu)
    except:
        node = dnaLoader.loadDNAFile(dnaStorage, fileo)
    if node.node().getNumChildren() > 0:
        return node.node()
    return None

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    fileu = '../resources/' + file
    fileo = 'resources/' + file
    try:
        data = dnaLoader.loadDNAFileAI(dnaStorage, fileu)
    except:
        data = dnaLoader.loadDNAFileAI(dnaStorage, fileo)
    return data

def setupDoor(a, b, c, d, e, f):
    try:
        e = int(str(e).split('_')[0])
        
    except:
        print 'setupDoor: error parsing', e
        e = 9999
        
    DNADoor.setupDoor(a, b, c, d, e, f)

