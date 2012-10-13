from enigma import *
from Screens.Screen import Screen
from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap
from __init__ import _, loadPluginSkin

class AboutTeam(Screen):

    def __init__(self, session, args = 0):
        Screen.__init__(self, session)
        abouttxt = '\nXtrend Support Team:\n\n- babsy98 (Main Developer)\n- xtrendmaster (Graphics and Skin) \n\nBetatesting:\n\n- Xtrend-Support Beta Team\n\nFurther credits goes to:\n\n- OpenPli\n- SIFTeam\n- openVix\n- openAAF\n- OE-Alliance\n'
        self['about'] = Label(abouttxt)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.quit}, -2)

    def quit(self):
        self.close()