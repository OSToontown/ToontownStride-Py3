from direct.stdpy import threading
from direct.showbase.ShowBase import ShowBase
from panda3d.core import VirtualFileSystem
import __builtin__, wx, os, sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../../"
        )
    )
)

__builtin__.__dict__.update(__import__('pandac.PandaModules', fromlist=['*']).__dict__)

loadPrcFile('dependencies/config/guieditor.prc')
loadPrcFile('dependencies/config/general.prc')

defaultText = """from pandac.PandaModules import *
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals

DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
"""

exec(
    "from %s import %s as imported" % \
    (
        '.'.join(
            sys.argv[1].split('.')[:-1]
        ),
        sys.argv[1].split('.')[-1]
    )
)

if hasattr(imported, 'GUI_EDITOR'):
    defaultText += imported.GUI_EDITOR

__builtin__.base = ShowBase()

exec(defaultText)

base.run()
