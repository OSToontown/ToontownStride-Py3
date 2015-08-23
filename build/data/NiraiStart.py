from panda3d.core import *
import __builtin__, os, sys
import aes

import niraidata

# Config
prc = niraidata.CONFIG
iv, key, prc = prc[:16], prc[16:32], prc[32:]
prc = aes.decrypt(prc, key, iv)

for line in prc.split('\n'):
    line = line.strip()
    if line:
        loadPrcFileData('nirai config', line)

del prc
del iv
del key

# DC
__builtin__.dcStream = StringStream()

dc = niraidata.DC
iv, key, dc = dc[:16], dc[16:32], dc[32:]
dc = aes.decrypt(dc, key, iv)

dcStream.setData(dc)
del dc
del iv
del key

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
#from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

# Resources
# TO DO: Sign and verify the phases to prevent edition
abort = False

# Packs
pack = os.environ.get('TT_STRIDE_CONTENT_PACK')
import glob
if pack and pack != 'default':
    print 'Loading content pack', pack
    for file in glob.glob('resources/%s/*.mf' % pack):
        mf = Multifile()
        mf.openReadWrite(Filename(file))
        names = mf.getSubfileNames()
        for name in names:
            ext = os.path.splitext(name)[1]
            if ext not in ['.jpg', '.jpeg', '.ogg', '.rgb']:
                mf.removeSubfile(name)
        vfs.mount(mf, Filename('/'), 0)

if not abort:
    # Run
    import toontown.toonbase.ToontownStart
