from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Button import Button
from Components.ScrollLabel import ScrollLabel
from Components.MenuList import MenuList
from Extra.BoxInfo import BoxInfo
from os import system, listdir
from __init__ import _, loadPluginSkin

class Scripts(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        boxinfo = BoxInfo()
        boxinfo.detectBox()
        self.scriptsPath = boxinfo.scriptsPath
        self['statuslab'] = Label('')
        self['key_red'] = Button(_('Execute'))
        self['key_green'] = Button('')
        self['key_yellow'] = Button('')
        self['key_blue'] = Button(_('Exit'))
        self.mlist = []
        try:
            self.populateSL()
        except OSError:
            print '[CTPanel] Could not find any /usr/script Folder to populate'

        self['list'] = MenuList(self.mlist)
        self['list'].onSelectionChanged.append(self.schanged)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.mygo,
         'back': self.close,
         'blue': self.close,
         'red': self.mygo})
        self.onLayoutFinish.append(self.refr_sel)

    def refr_sel(self):
        self['list'].moveToIndex(1)
        self['list'].moveToIndex(0)

    def populateSL(self):
        self.scriptdesc = []
        try:
            myscripts = listdir(self.scriptsPath)
            print myscripts
            for fil in myscripts:
                if fil.find('.sh') != -1:
                    fil2 = fil[:-3]
                    desc = 'N/A'
                    print self.scriptsPath + fil
                    f = open(self.scriptsPath + fil, 'r')
                    for line in f.readlines():
                        if line.find('#DESCRIPTION=') != -1:
                            line = line.strip()
                            desc = line[13:]

                    f.close()
                    self.mlist.append(fil2)
                    self.scriptdesc.append(desc)

        except OSError:
            print '[CTPanel] Could not find any /usr/script Folder to populate'

    def schanged(self):
        mysel = self['list'].getSelectedIndex()
        if mysel >= 0 and mysel < len(self.scriptdesc):
            self['statuslab'].setText(self.scriptdesc[mysel])

    def mygo(self):
        if self['list'].getSelectedIndex() >= 0 and self['list'].getSelectedIndex() < len(self.scriptdesc):
            mysel = self['list'].getCurrent()
            mysel2 = self.scriptsPath + mysel + '.sh'
            mytitle = 'Script: ' + mysel
            self.session.open(Console, title=mytitle, cmdlist=[mysel2])