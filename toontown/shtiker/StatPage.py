from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog
import ShtikerPage

STATS = ['cog', 'v2', 'skele', 'beanSpent', 'beanEarnt', 'task', 'vp', 'cfo', 'cj', 'ceo', 'sad', 'bldg', 'cogdo', 'item', 'fish', 'flower', 'race', 'golf', 'sos', 'unite', 'slip', 'gag']

class StatPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.dialog = None

    def load(self):
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')

        self.rows = [None] * 2
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.StatPageTitle, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        self.rows[0] = DirectLabel(parent=self, relief=None, text_align=TextNode.ALeft, text='', text_scale=0.06, text_wordwrap=16, pos=(-0.8, 0, 0.515))
        self.rows[1] = DirectLabel(parent=self, relief=None, text_align=TextNode.ALeft, text='', text_scale=0.06, text_wordwrap=16, pos=(0.05, 0, 0.515))
        self.resetButton = empty = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.1, 1, 1), text='Reset stats', text_scale=0.055, text_pos=(0, -0.02), pos=(-0.55, 0.0, 0.65), command=self.__showDialog)
        guiButton.removeNode()

    def enter(self):
        self.show()
        self.updateStats()
        self.accept('refreshStats', self.updateStats)

    def exit(self):
        self.ignoreAll()
        self.unloadDialog()
        self.hide()
    
    def unload(self):
        for row in self.rows:
            row.destroy()
        
        del self.rows
        self.unloadDialog()
        self.title.destroy()
        del self.title
        self.resetButton.destroy()
        del self.resetButton
        ShtikerPage.ShtikerPage.unload(self)
    
    def unloadDialog(self, arg=None):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None

    def cutToChunks(self, list, size):
        for i in xrange(0, len(list), size):
            yield list[i:i+size]

    def updateStats(self):
        dict = {}
        stats = base.localAvatar.stats
        
        for i, string in enumerate(STATS):
            dict[string] = "{:,}".format(stats[i])
        
        textChunks = list(self.cutToChunks(TTLocalizer.Stats, 11))
        
        for i, chunk in enumerate(textChunks):
            self.rows[i]['text'] = '\n\n'.join(chunk) % dict
    
    def __showDialog(self):
        self.dialog = TTDialog.TTDialog(style=TTDialog.TwoChoice, text=TTLocalizer.StatResetAsk, text_wordwrap=15, command=self.__handleDialogResponse)
        self.dialog.show()
    
    def __handleDialogResponse(self, response):
        self.unloadDialog()
        
        if response <= 0:
            return
        
        base.localAvatar.wipeStats()
        self.dialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=TTLocalizer.StatResetDone, text_wordwrap=15, command=self.unloadDialog)
        self.dialog.show()