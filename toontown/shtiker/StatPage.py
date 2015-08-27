from direct.gui.DirectGui import *
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog
import ShtikerPage

class StatPage(ShtikerPage.ShtikerPage):
    def __init__(self):

        ShtikerPage.ShtikerPage.__init__(self)
        self.dialog = None
        self.chunkCount = 11
        base.cr.lol = self

    def load(self):
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')

        self.rows = [self.createRow(pos) for pos in ((-0.8, 0, 0.435), (0.08, 0, 0.435))]
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.StatPageTitle, text_scale=0.12, textMayChange=0, pos=(-0.625, 0, 0.625))
        self.resetButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.1, 1, 1), text=TTLocalizer.StatPageClear, text_scale=0.055, text_pos=(0, -0.02), pos=(0.605, 0, 0.66), command=self.__showDialog)
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
    
    def createRow(self, pos):
        row = DirectLabel(parent=self, relief=None, text_align=TextNode.ALeft, text='', text_scale=0.045, text_wordwrap=16, text_font=ToontownGlobals.getChalkFont(), text_fg=(1, 1, 1, 1), image='phase_3/maps/stat_board.png', image_scale=(0.42, 0, 0.6), image_pos=(0.35, 0, -0.45))
        row.setPos(pos)
        return row

    def cutToChunks(self, list, size):
        for i in xrange(0, len(list), size):
            yield list[i:i+size]

    def updateStats(self):
        stats = base.localAvatar.stats
        allStats = [TTLocalizer.Stats[i] % stats[i] for i in xrange(len(stats))]
        textChunks = list(self.cutToChunks(allStats, self.chunkCount))
        
        for i, chunk in enumerate(textChunks):
            self.rows[i]['text'] = '\n\n'.join(chunk)
    
    def __showDialog(self):
        self.dialog = TTDialog.TTDialog(style=TTDialog.TwoChoice, text=TTLocalizer.StatPageClearAsk, text_wordwrap=15, command=self.__handleDialogResponse)
        self.dialog.show()
    
    def __handleDialogResponse(self, response):
        self.unloadDialog()
        
        if response <= 0:
            return
        
        base.localAvatar.wipeStats()
        self.dialog = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=TTLocalizer.StatPageClearDone, text_wordwrap=15, command=self.unloadDialog)
        self.dialog.show()