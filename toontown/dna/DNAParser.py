from direct.stdpy import threading

import DNALoader
from DNAStorage import DNAStorage
from DNASuitPoint import DNASuitPoint
from DNAGroup import DNAGroup
from DNAVisGroup import DNAVisGroup
from DNADoor import DNADoor

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
    dnaLoader = DNALoader.DNALoader()
    fileu = '../resources/' + file
    fileo = 'resources/' + file
    try:
        dnaLoader.loadDNAFile(dnaStorage, fileu)
    except:
        dnaLoader.loadDNAFile(dnaStorage, fileo)
    dnaLoader.destroy()

def loadDNAFile(dnaStorage, file):
    print 'Reading DNA file...', file
    dnaLoader = DNALoader.DNALoader()
    fileu = '../resources/' + file
    fileo = 'resources/' + file
    try:
        node = dnaLoader.loadDNAFile(dnaStorage, fileu)
    except:
        node = dnaLoader.loadDNAFile(dnaStorage, fileo)
    dnaLoader.destroy()
    if node.node().getNumChildren() > 0:
        return node.node()
    return None

def loadDNAFileAI(dnaStorage, file):
    dnaLoader = DNALoader.DNALoader()
    fileu = '../resources/' + file
    fileo = 'resources/' + file
    try:
        data = dnaLoader.loadDNAFileAI(dnaStorage, fileu)
    except:
        data = dnaLoader.loadDNAFileAI(dnaStorage, fileo)
    dnaLoader.destroy()
    return data

