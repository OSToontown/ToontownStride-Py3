from direct.directnotify import DirectNotifyGlobal
import LoginBase

class LoginTTUAccount(LoginBase.LoginBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginTTUAccount')

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def supportsRelogin(self):
        return 1

    def authorize(self, username, password):
        return 0 # No error!

    def sendLoginMsg(self):
        cr = self.cr
        # TODO

    def getErrorCode(self):
        return 0

    def authenticateDelete(self, loginName, password):
        return 1
