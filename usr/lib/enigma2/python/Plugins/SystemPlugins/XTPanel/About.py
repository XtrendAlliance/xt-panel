from enigma import *
from Screens.Screen import Screen
from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap
from __init__ import _, loadPluginSkin

class AboutTeam(Screen):

    def __init__(self, session, args = 0):
        Screen.__init__(self, session)
        abouttxt = '\nXtrend-Alliance Team:\n\nch3wb4kka (Developer) \nmmark (Graphics and Skin) \n\n- Betatesting:\n master, biki3, teckl, csm, vulcano5766, Gabriella.\n\nFurther credits goes to:\nxtrendboss for his constant support\n\n- openPLi\n- openVix\n- openATV\n - OE-Alliance\n'
        self['about'] = Label(abouttxt)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.quit}, -2)

    def quit(self):
        self.close()
