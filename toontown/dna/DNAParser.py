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
    fileu = 'resources/' + file
    dnaLoader.loadDNAFile(dnaStorage, fileu)

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader()
    fileu = 'resources/' + file
    node = dnaLoader.loadDNAFile(dnaStorage, fileu)
    if node.node().getNumChildren() > 0:
        return node.node()

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader()
    fileu = 'resources/' + file
    data = dnaLoader.loadDNAFileAI(dnaStorage, fileu)
    return data

def setupDoor(a, b, c, d, e, f):
    try:
        e = int(str(e).split('_')[0])
    except:
        print 'setupDoor: error parsing', e
        e = 9999

    DNADoor.setupDoor(a, b, c, d, e, f)
