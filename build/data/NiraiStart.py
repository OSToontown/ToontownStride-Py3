from panda3d.core import *
import __builtin__, os
import rc4

import niraidata

# Config
prc = niraidata.CONFIG
key, prc = prc[:32], prc[32:]
rc4.rc4_setkey(key)
prc = rc4.rc4(prc)

for line in prc.split('\n'):
    line = line.strip()
    if line:
        loadPrcFileData('nirai config', line)
    
del prc
    
# DC
__builtin__.dcStream = StringStream()

dc = niraidata.DC
key, dc = dc[:32], dc[32:]
rc4.rc4_setkey(key)
dc = rc4.rc4(dc)

dcStream.setData(dc)
del dc
rc4.rc4_setkey('\0\0\0\0')

# Resources
# TO DO: sign and verify the phases to prevent edition

vfs = VirtualFileSystem.getGlobalPtr()
mfs = (3, 3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13)
abort = False

for mf in mfs:
    filename = 'resources/default/phase_%s.mf' % mf
    if not os.path.isfile(filename):
        print 'Phase %s not found' % filename 
        abort = True
        break
        
    mf = Multifile()
    mf.openRead(filename)
        
    if not vfs.mount(mf, '../resources', 0):
        print 'Unable to mount %s' % filename
        abort = True
        break
            
# Packs
pack = os.environ.get('TT_STRIDE_CONTENT_PACK')
if pack and pack != 'default':
    print 'Loading content pack', pack
    for file in glob.glob('resources/%s/*.mf' % pack):
        mf = Multifile()
        mf.openReadWrite(Filename(file))
        names = mf.getSubfileNames()
        for name in names:
            ext = os.path.splitext(name)[1]
            if ext not in ('.jpg', '.jpeg', '.ogg', '.rgb'):
                mf.removeSubfile(name)
                
        mf.flush()
            
        if not vfs.mount(mf, '../resources', 0):
            print 'Unable to mount %s' % filename
            abort = True
            break
  
if not abort:
    # Run
    import toontown.toonbase.ClientStart
